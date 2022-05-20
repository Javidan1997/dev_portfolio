using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Parviz_Web_app.Areas.Manage.ViewModels;
using Parviz_Web_app.DAL;
using Parviz_Web_app.Helpers;
using Parviz_Web_app.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.Areas.Manage.Controllers
{
    [Area("manage")]
    [Authorize(Roles = "Admin", AuthenticationSchemes = "Admin_Auth")]
    public class PortfolioController : Controller
    {
        private readonly AppDbContext _context;
        private readonly IWebHostEnvironment _env;

        public PortfolioController(AppDbContext context, IWebHostEnvironment env)
        {
            _context = context;
            _env = env;
        }

        public async Task<IActionResult> Index()
        {
            TattooViewModel TattooVM = new TattooViewModel
            {
                Tattoos = await _context.Tattoos.ToListAsync()
            };

            return View(TattooVM);
        }
        public async Task<IActionResult> Create()
        {
            ViewBag.Categories = await _context.Categories.ToListAsync();
            return View();
        }



        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Create(Tattoo Tattoo)
        {


            #region CheckModelState
            if (!ModelState.IsValid)
            {
                return View(Tattoo);
            }
            #endregion


            if (Tattoo.File != null)
            {
                #region CheckFileLength
                if (Tattoo.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (Tattoo.File.ContentType != "image/png" && Tattoo.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion


                string filename = FileManager.Save(_env.WebRootPath, "uploads/Tattoo", Tattoo.File);

                Tattoo.Photo = filename;
            }

            await _context.Tattoos.AddAsync(Tattoo);
            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }

        public async Task<IActionResult> Edit(int id)
        {
            Tattoo Tattoo = await _context.Tattoos.FirstOrDefaultAsync(x => x.Id == id);

            #region CheckTattooNotFound
            if (Tattoo == null)
            {
                return NotFound();
            }
            #endregion
            ViewBag.Categories = await _context.Categories.ToListAsync();
            return View(Tattoo);

        }

        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Edit(Tattoo Tattoo)
        {
            Tattoo existTattoo = await _context.Tattoos.FirstOrDefaultAsync(x => x.Id == Tattoo.Id);

            #region CheckTattooNotFound
            if (existTattoo == null)
            {
                return NotFound();
            }
            #endregion

            existTattoo.Desc = Tattoo.Desc;
            existTattoo.Name = Tattoo.Name;
            existTattoo.CategoryId = Tattoo.CategoryId;



            if (Tattoo.File != null)
            {
                #region CheckFileLength
                if (Tattoo.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (Tattoo.File.ContentType != "image/png" && Tattoo.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion

                string filename = FileManager.Save(_env.WebRootPath, "uploads/tattoo", Tattoo.File);

                if (!string.IsNullOrWhiteSpace(existTattoo.Photo))
                {
                    FileManager.Delete(_env.WebRootPath, "uploads/tattoo", existTattoo.Photo);
                }

                existTattoo.Photo = filename;
            }
            else if (string.IsNullOrWhiteSpace(Tattoo.Photo))
            {
                FileManager.Delete(_env.WebRootPath, "uploads/tattoo", existTattoo.Photo);

                existTattoo.Photo = null;
            }

            ViewBag.Categories = await _context.Categories.ToListAsync();
            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }
    }
}

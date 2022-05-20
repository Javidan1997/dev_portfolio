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
    public class RecentworkController : Controller
    {
        private readonly AppDbContext _context;
        private readonly IWebHostEnvironment _env;

        public RecentworkController(AppDbContext context, IWebHostEnvironment env)
        {
            _context = context;
            _env = env;
        }

        public async Task<IActionResult> Index()
        {
            RecentworkViewModel RecentworkVM = new RecentworkViewModel
            {
                Recentworks = await _context.Recentworks.ToListAsync()
            };

            return View(RecentworkVM);
        }
        public async Task<IActionResult> Create()
        {
            ViewBag.Categories = await _context.Categories.ToListAsync();
            return View();
        }



        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Create(Recentwork Recentwork)
        {


            #region CheckModelState
            if (!ModelState.IsValid)
            {
                return View(Recentwork);
            }
            #endregion


            if (Recentwork.File != null)
            {
                #region CheckFileLength
                if (Recentwork.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (Recentwork.File.ContentType != "image/png" && Recentwork.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion


                string filename = FileManager.Save(_env.WebRootPath, "uploads/recentwork", Recentwork.File);

                Recentwork.Photo = filename;
            }

            await _context.Recentworks.AddAsync(Recentwork);
            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }

        public async Task<IActionResult> Edit(int id)
        {
            Recentwork Recentwork = await _context.Recentworks.FirstOrDefaultAsync(x => x.Id == id);

            #region CheckRecentworkNotFound
            if (Recentwork == null)
            {
                return NotFound();
            }
            #endregion
            ViewBag.Categories = await _context.Categories.ToListAsync();
            return View(Recentwork);

        }

        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Edit(Recentwork Recentwork)
        {
            Recentwork existRecentwork = await _context.Recentworks.FirstOrDefaultAsync(x => x.Id == Recentwork.Id);

            #region CheckRecentworkNotFound
            if (existRecentwork == null)
            {
                return NotFound();
            }
            #endregion

            existRecentwork.Desc = Recentwork.Desc;
            existRecentwork.Name = Recentwork.Name;
            existRecentwork.CategoryId = Recentwork.CategoryId;



            if (Recentwork.File != null)
            {
                #region CheckFileLength
                if (Recentwork.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (Recentwork.File.ContentType != "image/png" && Recentwork.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion

                string filename = FileManager.Save(_env.WebRootPath, "uploads/recentwork", Recentwork.File);

                if (!string.IsNullOrWhiteSpace(existRecentwork.Photo))
                {
                    FileManager.Delete(_env.WebRootPath, "uploads/recentwork", existRecentwork.Photo);
                }

                existRecentwork.Photo = filename;
            }
            else if (string.IsNullOrWhiteSpace(Recentwork.Photo))
            {
                FileManager.Delete(_env.WebRootPath, "uploads/recentwork", existRecentwork.Photo);

                existRecentwork.Photo = null;
            }

            ViewBag.Categories = await _context.Categories.ToListAsync();
            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }
    }
}

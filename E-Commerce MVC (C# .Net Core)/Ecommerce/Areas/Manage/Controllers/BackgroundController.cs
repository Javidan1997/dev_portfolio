using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
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
    public class BackgroundController : Controller
    {
        private readonly AppDbContext _context;
        private readonly IWebHostEnvironment _env;

        public BackgroundController(AppDbContext context, IWebHostEnvironment env)
        {
            _context = context;
            _env = env;
        }

        public async Task<IActionResult> Index()
        {
            BackgroundViewModel backgroundVM = new BackgroundViewModel
            {
                Backgrounds = await _context.Backgrounds.ToListAsync()
            };

            return View(backgroundVM);
        }

       

        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Create(Background background)
        {
           

            #region CheckModelState
            if (!ModelState.IsValid)
            {
                return View(background);
            }
            #endregion


            if (background.File != null)
            {
                #region CheckFileLength
                if (background.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (background.File.ContentType != "image/png" && background.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion


                string filename = FileManager.Save(_env.WebRootPath, "uploads/background", background.File);

                background.Photo = filename;
            }
         
            await _context.Backgrounds.AddAsync(background);
            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }

        public async Task<IActionResult> Edit(int id)
        {
            Background background = await _context.Backgrounds.FirstOrDefaultAsync(x => x.Id == id);

            #region CheckBackgroundNotFound
            if (background == null)
            {
                return NotFound();
            }
            #endregion

            return View(background);

        }

        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Edit(Background background)
        {
            Background existBackground = await _context.Backgrounds.FirstOrDefaultAsync(x => x.Id == background.Id);

            #region CheckBackgroundNotFound
            if (existBackground == null)
            {
                return NotFound();
            }
            #endregion

            existBackground.Title = background.Title;
            existBackground.SubTitle = background.SubTitle;
            




            if (background.File != null)
            {
                #region CheckFileLength
                if (background.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (background.File.ContentType != "image/png" && background.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion

                string filename = FileManager.Save(_env.WebRootPath, "uploads/background", background.File);

                if (!string.IsNullOrWhiteSpace(existBackground.Photo))
                {
                    FileManager.Delete(_env.WebRootPath, "uploads/background", existBackground.Photo);
                }

                existBackground.Photo = filename;
            }
            else if (string.IsNullOrWhiteSpace(background.Photo))
            {
                FileManager.Delete(_env.WebRootPath, "uploads/background", existBackground.Photo);

                existBackground.Photo = null;
            }


            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }

       
  



     

    }
}

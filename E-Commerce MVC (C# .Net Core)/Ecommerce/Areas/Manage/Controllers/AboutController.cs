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
    public class AboutController : Controller
    {
        private readonly AppDbContext _context;
        private readonly IWebHostEnvironment _env;

        public AboutController(AppDbContext context, IWebHostEnvironment env)
        {
            _context = context;
            _env = env;
        }

        public async Task<IActionResult> Index()
        {
            AboutViewModel AboutVM = new AboutViewModel
            {
                Abouts = await _context.Abouts.ToListAsync()
            };

            return View(AboutVM);
        }



        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Create(About About)
        {


            #region CheckModelState
            if (!ModelState.IsValid)
            {
                return View(About);
            }
            #endregion


            if (About.File != null)
            {
                #region CheckFileLength
                if (About.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (About.File.ContentType != "image/png" && About.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion


                string filename = FileManager.Save(_env.WebRootPath, "uploads/about", About.File);

                About.Photo = filename;
            }

            await _context.Abouts.AddAsync(About);
            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }

        public async Task<IActionResult> Edit(int id)
        {
            About About = await _context.Abouts.FirstOrDefaultAsync(x => x.Id == id);

            #region CheckAboutNotFound
            if (About == null)
            {
                return NotFound();
            }
            #endregion

            return View(About);

        }

        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Edit(About About)
        {
            About existAbout = await _context.Abouts.FirstOrDefaultAsync(x => x.Id == About.Id);

            #region CheckAboutNotFound
            if (existAbout == null)
            {
                return NotFound();
            }
            #endregion

            existAbout.Title = About.Title;
            existAbout.SubTitle = About.SubTitle;
            existAbout.Desc = About.Desc;




            if (About.File != null)
            {
                #region CheckFileLength
                if (About.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (About.File.ContentType != "image/png" && About.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion

                string filename = FileManager.Save(_env.WebRootPath, "uploads/about", About.File);

                if (!string.IsNullOrWhiteSpace(existAbout.Photo))
                {
                    FileManager.Delete(_env.WebRootPath, "uploads/about", existAbout.Photo);
                }

                existAbout.Photo = filename;
            }
            else if (string.IsNullOrWhiteSpace(About.Photo))
            {
                FileManager.Delete(_env.WebRootPath, "uploads/about", existAbout.Photo);

                existAbout.Photo = null;
            }


            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }
    }
}

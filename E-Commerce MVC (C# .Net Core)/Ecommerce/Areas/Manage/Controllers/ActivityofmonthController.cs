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
    public class ActivityofmonthController : Controller
    {
        private readonly AppDbContext _context;
        private readonly IWebHostEnvironment _env;

        public ActivityofmonthController(AppDbContext context, IWebHostEnvironment env)
        {
            _context = context;
            _env = env;
        }

        public async Task<IActionResult> Index()
        {
            ActivityofmonthViewModel ActivityofmonthVM = new ActivityofmonthViewModel
            {
                Activityofmonths = await _context.Activityofmonths.ToListAsync()
            };

            return View(ActivityofmonthVM);
        }
        public async Task<IActionResult> Create()
        {
            ViewBag.Categories = await _context.Categories.ToListAsync();
            return View();
        }



        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Create(Activityofmonth Activityofmonth)
        {


            #region CheckModelState
            if (!ModelState.IsValid)
            {
                return View(Activityofmonth);
            }
            #endregion


            if (Activityofmonth.File != null)
            {
                #region CheckFileLength
                if (Activityofmonth.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (Activityofmonth.File.ContentType != "image/png" && Activityofmonth.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion


                string filename = FileManager.Save(_env.WebRootPath, "uploads/activityofmonth", Activityofmonth.File);

                Activityofmonth.Photo = filename;
            }

            await _context.Activityofmonths.AddAsync(Activityofmonth);
            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }

        public async Task<IActionResult> Edit(int id)
        {
            Activityofmonth Activityofmonth = await _context.Activityofmonths.FirstOrDefaultAsync(x => x.Id == id);

            #region CheckActivityofmonthNotFound
            if (Activityofmonth == null)
            {
                return NotFound();
            }
            #endregion
            ViewBag.Categories = await _context.Categories.ToListAsync();
            return View(Activityofmonth);

        }

        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Edit(Activityofmonth Activityofmonth)
        {
            Activityofmonth existActivityofmonth = await _context.Activityofmonths.FirstOrDefaultAsync(x => x.Id == Activityofmonth.Id);

            #region CheckActivityofmonthNotFound
            if (existActivityofmonth == null)
            {
                return NotFound();
            }
            #endregion

            existActivityofmonth.Desc = Activityofmonth.Desc;
            existActivityofmonth.Name = Activityofmonth.Name;
            existActivityofmonth.CategoryId = Activityofmonth.CategoryId;



            if (Activityofmonth.File != null)
            {
                #region CheckFileLength
                if (Activityofmonth.File.Length > 2 * (1024 * 1024))
                {
                    ModelState.AddModelError("File", "Should be less than 2mb");
                    return View();
                }
                #endregion

                #region CheckFileContentType
                if (Activityofmonth.File.ContentType != "image/png" && Activityofmonth.File.ContentType != "image/jpeg")
                {
                    ModelState.AddModelError("File", "Select file type properly");
                    return View();
                }
                #endregion

                string filename = FileManager.Save(_env.WebRootPath, "uploads/activityofmonth", Activityofmonth.File);

                if (!string.IsNullOrWhiteSpace(existActivityofmonth.Photo))
                {
                    FileManager.Delete(_env.WebRootPath, "uploads/activityofmonth", existActivityofmonth.Photo);
                }

                existActivityofmonth.Photo = filename;
            }
            else if (string.IsNullOrWhiteSpace(Activityofmonth.Photo))
            {
                FileManager.Delete(_env.WebRootPath, "uploads/activityofmonth", existActivityofmonth.Photo);

                existActivityofmonth.Photo = null;
            }

            ViewBag.Categories = await _context.Categories.ToListAsync();
            await _context.SaveChangesAsync();

            return RedirectToAction("index");
        }
    }
}

using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Parviz_Web_app.DAL;
using Parviz_Web_app.Models;
using Parviz_Web_app.ViewModels;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.Controllers
{
    public class HomeController : Controller
    {
        private readonly AppDbContext _context;
        public HomeController(AppDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            HomeViewModel homeVM = new HomeViewModel
            {
                About = _context.Abouts.ToList(),
                Twitter =_context.Twitters.ToList(),
                Instagram = _context.Instagrams.ToList(),
                SocialMedia = _context.SocialMedias.ToList(),
                Backgrounds = _context.Backgrounds.ToList(),
                RecentWorks = _context.Recentworks.Include(x => x.Category).ToList(),
                Tattoos = _context.Tattoos.Include(x => x.Category).ToList(),
                Activityofmonths = _context.Activityofmonths.Include(x => x.Category).ToList(),
                Peoples = _context.Peoples.ToList(),
                Contact = _context.Contacts.ToList()
            

            };

            return View(homeVM);
        }
    }
}
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.Areas.Manage.Controllers
{

        [Area("manage")]
        [Authorize(Roles = "Admin", AuthenticationSchemes = "Admin_Auth")]
        public class DashboardController : Controller
        {
            public IActionResult Index()
            {
                return View();
            }
        }
}


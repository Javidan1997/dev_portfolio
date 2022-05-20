using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.DependencyInjection;
using Parviz_Web_app.Areas.Manage.ViewModels;
using Parviz_Web_app.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;

namespace Parviz_Web_app.Areas.Manage
{
    [Area("manage")]
    public class AccountController : Controller
    {
        private readonly UserManager<AppUser> _userManager;
        private readonly RoleManager<IdentityRole> _roleManager;
        private readonly SignInManager<AppUser> _signInManager;

        public AccountController(UserManager<AppUser> userManager, RoleManager<IdentityRole> roleManager, SignInManager<AppUser> signInManager)
        {
            _userManager = userManager;
            _roleManager = roleManager;
            _signInManager = signInManager;
        }
        public IActionResult Login()
        {
            return View();
        }

        public async Task Create()
        {
            AppUser user = new AppUser
            {
                UserName = "SuperAdmin",
                FullName = "Super Admin",
            };

            await _userManager.CreateAsync(user, "Admin123");
            await _userManager.AddToRoleAsync(user, "Admin");

        }
    
        //private async Task CreateRoles(IServiceProvider serviceProvider)
        //{
        //    //initializing custom roles 
        //    var RoleManager = serviceProvider.GetRequiredService<RoleManager<IdentityRole>>();
        //    var UserManager = serviceProvider.GetRequiredService<UserManager<AppUser>>();
        //    string[] roleNames = { "Admin", "Store-Manager", "Member" };
        //    IdentityResult roleResult;

        //    foreach (var roleName in roleNames)
        //    {
        //        var roleExist = await RoleManager.RoleExistsAsync(roleName);
        //        // ensure that the role does not exist
        //        if (!roleExist)
        //        {
        //            //create the roles and seed them to the database: 
        //            roleResult = await RoleManager.CreateAsync(new IdentityRole(roleName));
        //        }
        //    }

        //    // find the user with the admin email 
        //    var _user = await UserManager.FindByEmailAsync("admin@email.com");

        //    // check if the user exists
        //    if (_user == null)
        //    {
        //        //Here you could create the super admin who will maintain the web app
        //        var poweruser = new AppUser
        //        {
        //            UserName = "Admin",
        //            Email = "admin@email.com",
        //        };
        //        string adminPassword = "p@$$w0rd";

        //        var createPowerUser = await UserManager.CreateAsync(poweruser, adminPassword);
        //        if (createPowerUser.Succeeded)
        //        {
        //            //here we tie the new user to the role
        //            await UserManager.AddToRoleAsync(poweruser, "Admin");

        //        }
        //    }
        //}
        public async Task CreateRole()
        {
            await _roleManager.CreateAsync(new IdentityRole { Name = "Admin" });
            await _roleManager.CreateAsync(new IdentityRole { Name = "Member" });

        }

        [HttpPost]
            [AutoValidateAntiforgeryToken]
            public async Task<IActionResult> Login(AdminLoginViewModel loginVM)
            {
                if (!ModelState.IsValid)
                {
                    return View();
                }

                AppUser admin = await _userManager.FindByNameAsync(loginVM.UserName);

                if (admin == null)
                {
                    ModelState.AddModelError("", "Username or Password is incorrect!");
                    return View();
                }

                if (await _userManager.CheckPasswordAsync(admin, loginVM.Password))
                {
                    ModelState.AddModelError("", "Username or Password is incorrect!");
                    return View();
                }


                ClaimsIdentity claimsIdentity = new ClaimsIdentity(new[]
                {
                new Claim(ClaimTypes.Name,admin.UserName),
                new Claim(ClaimTypes.Role,"Admin")
            }, "Admin_Auth");
                ClaimsPrincipal claimsPrincipal = new ClaimsPrincipal(claimsIdentity);
                await HttpContext.SignInAsync("Admin_Auth", claimsPrincipal);

                return RedirectToAction("index", "dashboard");
            }
        }
    }


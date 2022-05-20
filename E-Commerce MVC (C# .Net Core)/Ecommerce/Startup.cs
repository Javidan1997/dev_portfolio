using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Parviz_Web_app.DAL;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Newtonsoft;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Authentication;
using Parviz_Web_app.Models;
using Microsoft.AspNetCore.Identity;

namespace Parviz_Web_app
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        public void ConfigureServices(IServiceCollection services)
        {
            services.AddDbContext<AppDbContext>(option =>
            {
                option.UseSqlServer(Configuration.GetConnectionString("Default"));
            }).AddIdentity<AppUser, IdentityRole>(options =>
            {
                options.Password.RequireNonAlphanumeric = false;
                options.Password.RequireUppercase = false;
                options.Password.RequiredLength = 8;

            }).AddDefaultTokenProviders().AddEntityFrameworkStores<AppDbContext>();

            services.AddControllersWithViews()
                  .AddNewtonsoftJson(options =>
                  options.SerializerSettings.ReferenceLoopHandling = Newtonsoft.Json.ReferenceLoopHandling.Ignore);

            services.AddHttpContextAccessor();

            services.AddSession(options =>
            {
                options.IdleTimeout = TimeSpan.FromSeconds(10);
            });

            services.AddAuthentication(options =>
            {
                //options.DefaultScheme = "Member_Auth";
                //options.DefaultSignInScheme = "Member_Auth";
            })
         
          .AddCookie("Admin_Auth", options =>
          {
              options.LoginPath = "/manage/account/login";
              options.AccessDeniedPath = "/manage/account/login";
          });
        }

        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseHttpsRedirection();
            app.UseStaticFiles();
            app.UseRouting();
            app.UseAuthorization();
            app.UseDefaultFiles();
            app.UseSession();
            app.Use(async (context, next) =>
            {
                var area = context.Request.RouteValues["area"];
                string scheme = null;

                if (area != null)
                {

                    foreach (var item in context.Request.Cookies)
                    {
                        if (item.Key.Contains("Admin_Auth"))
                        {
                            scheme = "Admin_Auth";
                            break;
                        }
                    }
                }

                if (scheme != null)
                {
                    var result = await context.AuthenticateAsync(scheme);
                    if (result.Succeeded)
                    {
                        context.User = result.Principal;
                    }
                }

                await next();

            });


            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllerRoute(
                   name: "areas",
                   pattern: "{area:exists}/{controller=Home}/{action=Index}/{id?}"
                 );

                endpoints.MapControllerRoute(
                    name: "default",
                    pattern: "{controller=Home}/{action=Index}/{id?}");
            });
        }
    }
}
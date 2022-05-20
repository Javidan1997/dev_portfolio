using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Parviz_Web_app.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.DAL
{
    public class AppDbContext : IdentityDbContext<AppUser>
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {

        }

        public DbSet<About> Abouts { get; set; }
        public DbSet<Category> Categories { get; set; }
        public DbSet<Background> Backgrounds { get; set; }
        public DbSet<Instagram> Instagrams { get; set; }
        public DbSet<People> Peoples { get; set; }
        public DbSet<SocialMedia> SocialMedias { get; set; }
        public DbSet<Tattoo> Tattoos { get; set; }
        public DbSet<Twitter> Twitters { get; set; }
        public DbSet<Contact> Contacts { get; set; }
        public DbSet<Recentwork> Recentworks { get; set; }
        public DbSet<Activityofmonth> Activityofmonths { get; set; }
        public DbSet<AppUser> AppUsers { get; set; }
    }
}


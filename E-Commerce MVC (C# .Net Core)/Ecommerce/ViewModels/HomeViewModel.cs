using Parviz_Web_app.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.ViewModels
{
    public class HomeViewModel
    {
        public List<About> About { get; set; }
        public List<Background> Backgrounds { get; set; }
        public List<Recentwork> RecentWorks { get; set; }
        public List<Tattoo> Tattoos { get; set; }
        public List<Activityofmonth> Activityofmonths { get; set; }
        public List<People> Peoples { get; set; }
        public List<Twitter> Twitter { get; set; }
        public List<Instagram> Instagram { get; set; }
        public List<SocialMedia> SocialMedia { get; set; }
        public List<Contact> Contact { get; set; }
        

    }
}

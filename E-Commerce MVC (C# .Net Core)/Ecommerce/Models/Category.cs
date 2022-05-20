using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.Models
{
    public class Category:BaseEntity
    {

        [Required]
        [StringLength(maximumLength: 100)]
        public string Name { get; set; }

        public virtual ICollection<Tattoo> Tattoos { get; set; }
        public virtual ICollection<Recentwork> Recentworks { get; set; }
        public virtual ICollection<Activityofmonth> Activityofmonths { get; set; }
    }
}

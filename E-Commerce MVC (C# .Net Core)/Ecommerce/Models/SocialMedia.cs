using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.Models
{
    public class SocialMedia:BaseEntity
    {
        [StringLength(maximumLength: 800)]
        public string FacebookLink { get; set; }

        [StringLength(maximumLength: 800)]
        public string TwitterLink { get; set; }

        [StringLength(maximumLength: 800)]
        public string GooglePlusLink { get; set; }

        [StringLength(maximumLength: 800)]
        public string PinterestLink { get; set; }
    }
}

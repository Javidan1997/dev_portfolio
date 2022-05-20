using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.Models
{
    public class Background:BaseEntity
    {
        [StringLength(maximumLength: 100)]
        public string Title { get; set; }

        [StringLength(maximumLength: 100)]
        public string SubTitle { get; set; }
        public string Photo { get; set; }

        [NotMapped]
        public IFormFile File { get; set; } 
      
    }
}

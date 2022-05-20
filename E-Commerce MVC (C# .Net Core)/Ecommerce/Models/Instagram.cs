using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.Models
{
    public class Instagram:BaseEntity
    {

        [StringLength(maximumLength: 150)]
        public string Name { get; set; }

        [StringLength(maximumLength: 1500)]
        public string Desc { get; set; }
        public string Photo { get; set; }

        [NotMapped]
        public IFormFile File { get; set; }
    }
}

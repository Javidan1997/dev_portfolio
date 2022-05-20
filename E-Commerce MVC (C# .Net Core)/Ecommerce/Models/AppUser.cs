using Microsoft.AspNetCore.Identity;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.Models
{
    public class AppUser : IdentityUser
    {
        [StringLength(maximumLength: 50)]
        public string FullName { get; set; }
        public bool IsMember { get; set; }
        public bool IsActive { get; set; }

        [NotMapped]
        [StringLength(maximumLength: 20), DataType(DataType.Password)]
        public string CurrentPassword { get; set; }

        [NotMapped]
        [StringLength(maximumLength: 20), DataType(DataType.Password)]
        public string Password { get; set; }

        [NotMapped]
        [StringLength(maximumLength: 20), DataType(DataType.Password), Compare(nameof(Password))]
        public string ConfirmPassword { get; set; }

    }
}

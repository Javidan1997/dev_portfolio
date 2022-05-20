using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace Parviz_Web_app.Areas.Manage.ViewModels
{
    public class AdminLoginViewModel
    {
        [StringLength(maximumLength: 20), Required]
        public string UserName { get; set; }

        [StringLength(maximumLength: 20), Required, DataType(DataType.Password)]
        public string Password { get; set; }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Query.API.Kernel.Domain.Contracts.DTOs
{
    public class DatabaseRowDto
    {
        public Dictionary<string, object> Fields { get; set; }
    }
}

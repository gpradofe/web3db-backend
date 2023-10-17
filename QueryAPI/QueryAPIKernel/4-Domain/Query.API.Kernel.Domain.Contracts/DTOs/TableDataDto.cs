using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Query.API.Kernel.Domain.Contracts.DTOs
{
    public class TableDataDto
    {
        public List<DatabaseRowDto> Rows { get; set; }
        public Dictionary<string, string> Columns { get; set; }
    }
}

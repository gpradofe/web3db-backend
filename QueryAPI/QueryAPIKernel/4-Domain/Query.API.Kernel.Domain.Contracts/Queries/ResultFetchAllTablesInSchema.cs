using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Query.API.Kernel.Domain.Contracts.Queries
{
    public class ResultFetchAllTablesInSchema
    {
        List<string> Tables { get; set; }
    }
}

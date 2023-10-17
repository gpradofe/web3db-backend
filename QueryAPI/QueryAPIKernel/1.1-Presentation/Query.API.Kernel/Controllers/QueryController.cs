using Microsoft.AspNetCore.Mvc;
using Query.API.Kernel.Service.Core.APIBASE.StartupConfiguration.Base;
using Serilog.Context;

namespace Query.API.Kernel.Controllers
{
    public class QueryController : ApiControllerBase<QueryController>
    {
        #region Attributes

        #endregion
        public QueryController(ILogger<QueryController> logger) : base(logger)
        {
            _logger = logger;
        }
        [HttpGet("FetchAllSchemas")]
        public async Task<IActionResult> FetchAllSchemas()
        {
            try
            {
                using (LogContext.PushProperty("Fetching all schemas ", ""))
                {
                    _logger.LogInformation("Fetch all schemas in a database");

                    var schemas = await _QueryApplication.GetAllSchemasInDatabase();
                    if (schemas != null && schemas.Any())
                    {
                        return Ok(schemas);
                    }
                    else
                    {
                        return NoContent();
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error on FetchAllSchemas");
                throw ex;
            }
        }
        [HttpGet("FetchAllTablesInASchemas")]
        public async Task<IActionResult> FetchAllTablesInSchema(string schema)
        {
            try
            {
                using (LogContext.PushProperty("Fetching all tables in schema", schema))
                {
                    _logger.LogInformation("Fetch all tables in a schema");

                    var tables = await _QueryApplication.GetAllTablesInSchema();
                    if (tables != null && tables.Any())
                    {
                        return Ok(tables);
                    }
                    else
                    {
                        return NoContent();
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error on FetchAllTablesInSchema");
                throw ex;
            }
        }
        [HttpGet("FetchAllTablesInASchemas")]
        public async Task<IActionResult> FetchTable(string tableName)
        {
            try
            {
                using (LogContext.PushProperty("Fetching table", tableName))
                {
                    _logger.LogInformation($"Fetch table: {tableName}");

                    var results = await _QueryApplication.FetchTable();
                    if (results != null && results.Any())
                    {
                        return Ok(results);
                    }
                    else
                    {
                        return NoContent();
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error on FetchTable");
                throw ex;
            }
        }
        [HttpPost("RunQuery")]
        public async Task<IActionResult> RunQuery()
        {
            try
            {
                using (LogContext.PushProperty("Fetching table", tableName))
                {
                    _logger.LogInformation($"Fetch table: {tableName}");

                    var results = await _QueryApplication.FetchTable();
                    if (results != null && results.Any())
                    {
                        return Ok(results);
                    }
                    else
                    {
                        return NoContent();
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error on FetchTable");
                throw ex;
            }
        }
    }
}

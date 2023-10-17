using Microsoft.AspNetCore.Mvc.ApiExplorer;
using Query.API.Kernel.Service.Core.APIBASE.StartupConfiguration;
using Query.API.Kernel.Service.Core.APIBASE.StartupConfiguration.Swagger;
namespace Query.API.Kernel
{
    public class Startup
    {
        #region Constructor
        public Startup(IConfiguration configuration)
        {
            _configuration = configuration;

        }
        #endregion
        #region Attributes
        public IConfiguration _configuration { get; }
        #endregion
        #region Methods
        //This method gets called by the runtime. Use this method to add services to the container.

        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllers();
            services.AddApiVersioning(ver =>
            {
                ver.ReportApiVersions = true;
                ver.AssumeDefaultVersionWhenUnspecified = true;
            });
            services.AddVersionedApiExplorer(ver =>
            {
                ver.SubstituteApiVersionInUrl = true;
            });
            services.AddExtensions(_configuration);

            services.AddMvc(setupAction =>
            {
                setupAction.EnableEndpointRouting = false;
            }).AddJsonOptions(jsonOptions =>
            {
                jsonOptions.JsonSerializerOptions.PropertyNamingPolicy = null;
            });
            // services.InitializeRedisDatabase(_configuration);
            services.AddCors(options =>
            {
                options.AddDefaultPolicy(
                    builder =>
                    {
                        builder.AllowAnyOrigin();
                    });
            });

        }

        //This method gets called by the runtime. Use this method to add services to the container.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env, IApiVersionDescriptionProvider provider)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            app.UseHealthChecks("/healthycheck");
            app.UseHttpsRedirection();
            app.UseRouting();
            app.AddSwaggers(provider);
            app.UseAuthorization();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
            app.UseCors(x => x
                .AllowAnyMethod()
                .AllowAnyHeader()
                .SetIsOriginAllowed(origin => true)
                .AllowCredentials());
        }
        #endregion

    }
}

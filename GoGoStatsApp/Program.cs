using GoGoStatsApp.Components;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
}

app.Map("/gogostats", gogostatsApp =>
{
    gogostatsApp.UseRouting();

    gogostatsApp.UseStaticFiles();
    gogostatsApp.UseAntiforgery();

    gogostatsApp.UseEndpoints(endPoints =>
    {
        endPoints.MapRazorComponents<App>()
            .AddInteractiveServerRenderMode();
    });
});

app.Run();

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenApi();
builder.Services.AddHttpClient();
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
        policy.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseCors();
app.UseHttpsRedirection();

// Connected to Python Compliance Engine (http://localhost:8000)
app.MapPost("/api/scan", async (ScanRequest request, IHttpClientFactory clientFactory) =>
{
    var client = clientFactory.CreateClient();
    try
    {
        var response = await client.PostAsJsonAsync("http://localhost:8000/api/scan", request);
        if (response.IsSuccessStatusCode)
        {
            var data = await response.Content.ReadFromJsonAsync<object>();
            return Results.Ok(data);
        }
    }
    catch (Exception ex)
    {
        // Fallback if Python engine is offline
        Console.WriteLine($"Error reaching Python Compliance Engine: {ex.Message}");
    }

    return Results.Ok(new
    {
        productId = request.ProductId,
        status = "WARNING",
        is_compliant = false,
        note = "Python Compliance Engine offline fallback"
    });
});

app.Run();

record ScanRequest(string ProductId, string? Composition = null);
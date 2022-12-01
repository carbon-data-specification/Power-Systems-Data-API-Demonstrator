
namespace LFEnergy.Controllers
{
    using Microsoft.AspNetCore.Mvc;
    using System.Collections.Generic;

    [ApiController]
    [Route("[controller]")]
    public class SystemController : ControllerBase
    {
        private readonly ILogger<SystemController> _logger;

        public SystemController(ILogger<SystemController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        [Route("/generation")]
        public IEnumerable<Generation> GetGeneration()
        {
            Generation entry= new Generation()
            {
                PowerPerFuelType = new Dictionary<FuelType, uint>()
                {
                    { FuelType.Solar, 3457 },
                    { FuelType.Wind, 1650 },
                    { FuelType.BrownCoal, 432 }
                },
                Region = "ES",
                TimeStamp = DateTime.UtcNow,
                TotalPower = 5107
            };

            return new List<Generation>() { entry };
        }

        [HttpGet]
        [Route("/imports")]
        public ImportExport GetImports()
        {
            return new ImportExport()
            {
                Region = "ES",
                TimeStamp = DateTime.UtcNow,
                TotalPower = 534,
                PowerPerImport = new Dictionary<string, uint>()
                {
                    { "FR", 534 }
                }
            };
        }

        [HttpGet]
        [Route("/exports")]
        public ImportExport GetExports()
        {
            return new ImportExport()
            {
                Region = "ES",
                TimeStamp = DateTime.UtcNow,
                TotalPower = 134,
                PowerPerImport = new Dictionary<string, uint>()
                {
                    { "FR", 134 }
                }
            };
        }

        [HttpGet]
        [Route("/emissions")]
        public Dictionary<Pollutant, uint> GetEmissions()
        {
            return new Dictionary<Pollutant, uint>()
            {
                { Pollutant.CO2, 432 }
            };
        }
    }
}
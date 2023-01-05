
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
        [Route("/gridNode/list")]
        public IEnumerable<GridNode> ListGridNodes()
        {
            // TODO add filtering by type
            GridNode sampleGridNode1 = new GridNode()
            {
                ID = "nwjefnwm:@",
                name = "ES",
                type = GridNodeType.System,
            };
            GridNode sampleGridNode2 = new GridNode()
            {
                ID = "wpfm[",
                name = "production_unit_coal",
                type = GridNodeType.ProductionUnit,
            };

            return new List<GridNode>() { sampleGridNode1, sampleGridNode2 };
        }

        [HttpGet]
        [Route("/gridNode/describe/{id}")]
        public GridNode DescribeGridNode()
        {
            // TODO find matching node
            GridNode sampleGridNode = new GridNode()
            {
                ID = "nwjefnwm:@",
                name = "ES",
                type = GridNodeType.System,
                generation = new Generation()
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
                },
                importExport = new ImportExport()
                {
                    Region = "ES",
                    TimeStamp = DateTime.UtcNow,
                    TotalPower = 534,
                    PowerPerImport = new Dictionary<string, uint>()
                    {
                        { "FR", 534 }
                    }
                }
            };

            return sampleGridNode;
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
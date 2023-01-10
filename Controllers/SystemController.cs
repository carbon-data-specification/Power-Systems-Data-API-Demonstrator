
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

            // TODO would need to filter only relevant information
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
        [Route("/gridNode/{id}/generation")]
        public Generation GetGridNodeGeneration()
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
            };

            return sampleGridNode.generation;
        }

        [HttpGet]
        [Route("/gridNode/{id}/imports")]
        public ImportExport GetGridNodeImports()
        {
            // TODO find matching node
            GridNode sampleGridNode = new GridNode()
            {
                ID = "nwjefnwm:@",
                name = "ES",
                type = GridNodeType.System,
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
            return sampleGridNode.importExport;
        }

        [HttpGet]
        [Route("/gridNode/{id}/exports")]
        public ImportExport GetGridNodeExports()
        {
            // TODO find matching node
            GridNode sampleGridNode = new GridNode()
            {
                ID = "nwjefnwm:@",
                name = "ES",
                type = GridNodeType.System,
                importExport = new ImportExport()
                {
                    Region = "ES",
                    TimeStamp = DateTime.UtcNow,
                    TotalPower = 134,
                    PowerPerImport = new Dictionary<string, uint>()
                    {
                        { "FR", 134 }
                    }
                }
            };
            return sampleGridNode.importExport;
        }

        [HttpGet]
        [Route("/gridNode/{id}/emissions")]
        public Emissions GetGridNodeEmissions()
        {
            // TODO find matching node
            GridNode sampleGridNode = new GridNode()
            {
                ID = "nwjefnwm:@",
                name = "ES",
                type = GridNodeType.System,
                emissions = new Emissions()
                {
                    EmissionsPerPolutant = new Dictionary<Pollutant, uint>()
                    {
                        { Pollutant.CO2, 432 }
                    }
                }
            };

            return sampleGridNode.emissions; 
        }
    }
}
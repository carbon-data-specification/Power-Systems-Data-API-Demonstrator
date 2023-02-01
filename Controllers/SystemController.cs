
namespace LFEnergy.Controllers
{
    using LFEnergy.Services;
    using Microsoft.AspNetCore.Mvc;
    using System.Collections.Generic;


    [ApiController]
    [Route("[controller]")]
    public class SystemController : ControllerBase
    {
        private readonly ILogger<SystemController> _logger;
        private NodeService _nodeService;

        public SystemController(ILogger<SystemController> logger)
        {
            _logger = logger;
            _nodeService = new NodeService();
        }

        
        [HttpGet]
        [Route("/gridNode/list")]
        public IEnumerable<GridNode> ListGridNodes([FromQuery] GridNodeType type)
        {
            return _nodeService.listByType(type);
        }

        [HttpGet]
        [Route("/gridNode/describe/{id}")]
        public GridNode DescribeGridNode(string id)
        {
            // read from file
            return _nodeService.GetById(id);
            
        }

        [HttpGet]
        [Route("/generation/gridNode/{id}")]
        public List<Generation> GetGridNodeGeneration(string id)
        {
            // TODO find matching node
            return _nodeService.GetById(id).generation;
        }

        [HttpGet]
        [Route("/imports/gridNode/{id}")]
        public List<ImportExport> GetGridNodeImports(string id)
        {
            // TODO (make distinct objects for import and export?)
            return _nodeService.GetById(id).importExport;
        }

        [HttpGet]
        [Route("/exports/gridNode/{id}")]
        public List<ImportExport> GetGridNodeExports(string id)
        {
            // TODO (make distinct objects for import and export?)
            return _nodeService.GetById(id).importExport;
        }

        [HttpGet]
        [Route("/emissions/gridNode/{id}")]
        public List<Emissions> GetGridNodeEmissions(string id)
        {
            return _nodeService.GetById(id).emissions;
        }
    }
}

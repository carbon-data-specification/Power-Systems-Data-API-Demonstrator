using System;
using System.Linq;
using static LFEnergy.Services.EiaCsvService;

namespace LFEnergy.Services
{
	public class NodeService
	{
        public List<GridNode> allGridNodes;

		public NodeService()
		{
            EiaCsvService eiaCsvService = new EiaCsvService();

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

            allGridNodes = new List<GridNode> { sampleGridNode1, sampleGridNode2 };
            allGridNodes = allGridNodes.Concat(eiaCsvService.gridNodes).ToList();
        }

        public List<GridNode> listByType(GridNodeType type)
        {
            return allGridNodes.Where(x => x.type == type).ToList();
        }

        public GridNode GetById(string id)
		{
            // TODO (enforce unique IDs and make this function more sensibly)
            return allGridNodes.Where(x => x.ID == id).ToList()[0];
           
		}
	}
}


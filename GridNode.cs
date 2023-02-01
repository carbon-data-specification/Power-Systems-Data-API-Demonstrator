namespace LFEnergy
{

    public class GridNode
	{
        public string ID { get; set; } = string.Empty;
        public string name { get; set; } = string.Empty;
        public GridNodeType type { get; set; } = GridNodeType.ProductionUnit;
        // Optional static data
        // Could use inheritance for fields that are specific to only one grid node type
        public string market { get; set; } = string.Empty;
        public int startYear { get; set; } = 0;
        public string ownerInformation { get; set; } = string.Empty;
        // TODO would be proper type
        public string location { get; set; } = string.Empty;

        // parenthood relations
        public List<GridNode> gridNodeParents { get; set; } = new List<GridNode> { };
        public List<GridNode> gridNodeChildren { get; set; } = new List<GridNode> { };

        // We would also need GET all nodes, with possibility to filter per type, name, parent, location etc

        public List<Generation> generation { get; set; } = new List<Generation>();
        // IF GridNodeType is not at system level should return that it can't be queried
        public Demand demand { get; set; } = new Demand();
        // IF GridNodeType is not at system level should return that it can't be queried
        public List<ImportExport> importExport { get; set; } = new List<ImportExport>();
        public List<Emissions> emissions { get; set; } = new List<Emissions>();
 
    }
}

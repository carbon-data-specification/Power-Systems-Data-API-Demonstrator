namespace LFEnergy
{
	public class GridNode
	{
        public string ID { get; set; } = string.Empty;
        public string Name { get; set; } = string.Empty;
        public GridNodeType Type { get; set; } = GridNodeType.ProductionUnit;

        // We would also need GET all nodes, with possibility to filter per type, name, parent, location etc
        // 

        // Below does not work probably
        public class Generation
        {
            public DateTime TimeStamp { get; set; } // in UTC

            public string Region { get; set; } = string.Empty;

            public uint TotalPower { get; set; } // in MW

            public Dictionary<FuelType, uint> PowerPerFuelType { get; set; } = new Dictionary<FuelType, uint>(); // in MW
        }

        public class Demand
        {
            // IF GridNodeType is not at system level should return that it can't be queried
            public DateTime TimeStamp { get; set; } // in UTC

            public string Region { get; set; } = string.Empty;

            public uint TotalPower { get; set; } // in MW
        }

        public class ImportExport
        {
            // IF GridNodeType is not at system level should return that it can't be queried
            public DateTime TimeStamp { get; set; } // in UTC

            public string Region { get; set; } = string.Empty;

            public uint TotalPower { get; set; } // in MW

            public Dictionary<string, uint> PowerPerImport { get; set; } = new Dictionary<string, uint>(); // in MW
        }

        public class Emissions
        {
            public Dictionary<Pollutant, uint> EmissionsPerPolutant { get; set; } = new Dictionary<Pollutant, uint>(); // in KG
        }
    }
}

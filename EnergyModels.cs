namespace LFEnergy
{
    public class Generation
    {
        public DateTime TimeStamp { get; set; } // in UTC

        public string Region { get; set; } = string.Empty;

        public uint TotalPower { get; set; } // in MW

        public Dictionary<FuelType, uint> PowerPerFuelType { get; set; } = new Dictionary<FuelType, uint>(); // in MW
    }

    public class Demand
    {
        public DateTime TimeStamp { get; set; } // in UTC

        public string Region { get; set; } = string.Empty;

        public uint TotalPower { get; set; } // in MW
    }

    public class ImportExport
    {
        public DateTime TimeStamp { get; set; } // in UTC

        public string Region { get; set; } = string.Empty;

        public int TotalPowerImported { get; set; } // in MW

        public int TotalPowerExported { get; set; } // in MW

        public Dictionary<string, uint> PowerPerImport { get; set; } = new Dictionary<string, uint>(); // in MW

        public Dictionary<string, uint> PowerPerExport { get; set; } = new Dictionary<string, uint>(); // in MW
    }

    public class Emissions
    {
        public Dictionary<Pollutant, uint> EmissionsPerPolutant { get; set; } = new Dictionary<Pollutant, uint>(); // in KG
    }
}
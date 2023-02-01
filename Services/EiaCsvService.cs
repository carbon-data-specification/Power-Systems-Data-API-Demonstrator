using System;
using System.Formats.Asn1;
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;

namespace LFEnergy.Services
{
	public class EiaCsvService
	{
        public List<GridNode> gridNodes;
		public EiaCsvService()
		{
            gridNodes = getGridNodesFromCsv();

        }
        public List<GridNode> getGridNodesFromCsv()
        {
            // It currently gets the list of grid nodes to generate based on unique regions in the generation file
            List<Generation> generation;
            using (var reader = new StreamReader("data/Power data for API spec/EIA/generation.csv"))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                csv.Context.RegisterClassMap<EiaGenerationMap>();
                generation = csv.GetRecords<Generation>().ToList();
            }

            // TODO (decide on import export signs and related logic)
            List<ImportExport> importExport;
            using (var reader = new StreamReader("data/Power data for API spec/EIA/imports_exports.csv"))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                csv.Context.RegisterClassMap<EiaImportExportMap>();
                importExport = csv.GetRecords<ImportExport>().ToList();
            }

            List<string> uniqueRegions = generation.Select(o => o.Region).Distinct().ToList();
            List<GridNode> gridNodes = new List<GridNode> { };
            for (int i = 0; i < uniqueRegions.Count; i++) {
                GridNode gridNode = new GridNode()
                {
                    ID = "EIA." + uniqueRegions[i],
                    name = "EIA." + uniqueRegions[i],
                    type = GridNodeType.System,
                    generation = generation.Where(x => x.Region == uniqueRegions[i]).ToList(),
                    importExport = importExport,
                    emissions = new List<Emissions>(){ },
                    // TODO (set all power plants as grid node children)
                    gridNodeChildren = new List<GridNode>() { }
                };
                gridNodes.Add(gridNode);
            }
            return gridNodes;
        }
	}


    public class EiaGenerationMap : ClassMap<Generation>
    {
        public EiaGenerationMap()
        {
            
            Map(m => m.Region).Name("Balancing Region");
            Map(m => m.TimeStamp).Name("datetime");
            Map(m => m.PowerPerFuelType).Convert(row =>
            {
                var dict = new Dictionary<FuelType, uint>();
                dict[FuelType.BrownCoal] = uint.Parse(row.Row.GetField("Coal (MW)"));
                dict[FuelType.Water] = uint.Parse(row.Row.GetField("Hydro (MW)"));
                // TODO (add other fuel types)
                return dict;
            });
            // TODO (add totalPower)
        }
    }

    public class EiaImportExportMap : ClassMap<ImportExport>
    {
        public EiaImportExportMap()
        {
            // TODO (add per-neighbor import/export)
            Map(m => m.TotalPowerExported).Name("export (MW)");
            Map(m => m.TotalPowerImported).Name("import (MW)");
            Map(m => m.TimeStamp).Name("datetime");
            Map(m => m.Region).Name("Balancing Region");

        }
    }

}



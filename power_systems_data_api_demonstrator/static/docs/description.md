<div class="aside">
    <img
        id="description-logo"
        src="https://artwork.lfenergy.org/projects/cdsc/horizontal/color/cdsc-horizontal-color.svg"
        alt="Carbon Data Specification Logo"
        />
</div>

Welcome to the **Power Systems Data API Demonstrator**!

This demonstrator is an API that serves power systems data according to the specification of the [Linux Foundation Carbon Data Specification Consortium](https://powersystemsdata.carbondataspec.org/).

Its goal is to demonstrate how the specification can be implemented by power system operators to share openly data about their power systems.

The demonstrator has been seeded with real power systems data from different operators.

## How to use

This page provides an overview of all the routes available in the API. For each route, you can find a description of the route, the parameters it accepts, and the response it returns.

An interactive environment, together with the real world seeded data allows to explore the API and its capabilities.

### Investigate Power System Resources

Most routes are dependent on the entity `PowerSystemResource`, which describes the geographical entity for which we want to explore power data.

The list of power system resources available in the demonstrator is available at [/PowerSystemResource/list](https://carbon-data-specification.onrender.com/gridNode/list). Further information about a specific power system resource can be found at [/PowerSystemResource/describe/{id}](https://carbon-data-specification.onrender.com/gridNode/UK-GB).

### Explore power data

With a power system resource selected, you can explore the power data available for that power system resource. Follow the routes below to explore the power data available for a specific power system resource.

_Disclaimer_: Some of the data for some of the endpoints might not have been seeded just yet.

## Useful links

- API documentation: [https://carbon-data-specification.onrender.com/redoc](https://carbon-data-specification.onrender.com/redoc)
- Specifications used to populate the API demonstrator:
  - Data Types: [https://github.com/carbon-data-specification/Power-Systems-Data/blob/main/datatypes.md](https://github.com/carbon-data-specification/Power-Systems-Data/blob/main/datatypes.md)
  - Grid Topology: [https://github.com/carbon-data-specification/Power-Systems-Data/blob/main/datatypes.md](https://github.com/carbon-data-specification/Power-Systems-Data/blob/main/topology.md)
- Carbon Data Specification Consortium: [https://github.com/carbon-data-specification?type=source](https://github.com/carbon-data-specification?type=source)

## Data sources

The data used in this demonstrator has been provided by the following operators:

- [ENTSO-E](https://transparency.entsoe.eu/)
- [EIA](https://www.eia.gov/electricity/data.php)
- [ELEXON](https://www.bmreports.com/bmrs/?q=help/about-us)

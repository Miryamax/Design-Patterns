using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Adapter
{
    public class City
    {
        public string FullName { get; set; }
        public long Inhabitants { get; set; }

        public City(string fullName, long inhabitants)
        {
            FullName = fullName;
            Inhabitants = inhabitants;
        }
    }

    public class CityFromExternalSystem
    {
        public string Name { get; set; }
        public string NickName { get; set; }
        public int Inhabitants { get; set; }

        public CityFromExternalSystem(string name, string nickName, int inhabitants)
        {
            Name = name;
            NickName = nickName;
            Inhabitants = inhabitants;
        }
    }

    public class ExternalSystem
    {
        public CityFromExternalSystem GetCity()
        {
            return new CityFromExternalSystem("Haifa", "Red-Haifa", 50000);
        }
    }

    public interface ICityAdapter
    {
        public City GetCity();
    }
   

    public class CityAdapter : ICityAdapter
    {
        ExternalSystem externalSystem;

        public CityAdapter(ExternalSystem externalSystem)
        {
            this.externalSystem = externalSystem;
        }

        public City GetCity()
        {
            CityFromExternalSystem city = externalSystem.GetCity();
            return new City($"{city.Name} {city.NickName}", city.Inhabitants);
        }
    }

    
   
}

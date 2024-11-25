using System.Security.Cryptography.X509Certificates;

namespace Strategy
{
    // the strategy
    public interface IExportService
    {
        void Export(Order order);
    }

    public class CSVExportService : IExportService
    {
        public void Export(Order order)
        {
            Console.WriteLine("export to CSV file");
        }
    }
    public class XMLExportService : IExportService
    {
        public void Export(Order order)
        {
            Console.WriteLine("export to XML file");
        }
    }

    public class JsonExportService : IExportService
    {
        public void Export(Order order)
        {
            Console.WriteLine("export to Json file");
        }
    }

    public class Order
    {
        private IExportService _exportService;

        public Order(IExportService exportService)
        {
            _exportService = exportService;
        }

        public void Export()
        {
            _exportService.Export(this);
        }
    }
}

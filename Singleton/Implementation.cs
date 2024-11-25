using System.Diagnostics;

namespace Singleton
{
    public class Logger
    {
       
        //private static Logger _instance;

        private static readonly Lazy<Logger> _lazyLogger = new Lazy<Logger>(() => new Logger());
        private Logger()
        {
        }

        public static Logger Instance()
        {
            //if (_instance == null)
            //    _instance = new Logger();
            //return _instance;
            return _lazyLogger.Value;
        }

        public void Log(string message)
        {
            Console.WriteLine(message);
        }

    }
  
}

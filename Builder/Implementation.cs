namespace BuilderPattern
{
    public interface CarPart
    {

    }
    public class Engine : CarPart
    {

    }

    public class Frame : CarPart
    {

    }

    public class Car
    {
        private string _type; 
        private List<CarPart> _parts= new List<CarPart>();
        public Car(string type)
        {
            _type = type;
        }
       public void AddPart(CarPart part)
        {
            _parts.Add(part);
        }
    }

    public abstract class CarBuilder
    {
        protected Car Car; 

        public CarBuilder(string carType)
        {
            Car  = new Car(carType);
        }
        public abstract void BuildFrame();
        public abstract void BuildEngine();
        public abstract Car GetCar();
    }

    public class MiniBuilder : CarBuilder
    {
        public MiniBuilder() : base("Mini")
        {
        }
        public override void BuildFrame()
        {
            Console.WriteLine("build frame...");
            Car.AddPart(new Frame());
        }

        public override void BuildEngine()
        {
            Console.WriteLine("build engine...");
            Car.AddPart(new Engine());
        }

        public override Car GetCar()
        {
            return Car;
        }

    }

    public class BMWBuilder : CarBuilder
    {
        public BMWBuilder() : base("BMW")
        {

        }
        public override void BuildFrame()
        {
            Console.WriteLine("build frame...");
            Car.AddPart(new Frame());
        }

        public override void BuildEngine()
        {
            Console.WriteLine("build engine...");
            Car.AddPart(new Engine());
        }

        public override Car GetCar()
        {
            return Car;
        }

    }

    public class Garage
    {
        private CarBuilder? _builder;

        public Garage(CarBuilder builder)
        {
            _builder = builder;
        }
    }

     
}

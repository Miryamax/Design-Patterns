namespace Facade
{

    // subsystem classes
    public class CustomerDiscountBaseService
    {
        // logic of calculate
    }

    public class DayOfTheWeekFactorService
    {
        // logic of calculate
    }
    public class DiscountFacade
    {
        // some members
        private readonly CustomerDiscountBaseService _customerDiscountBaseService;
        private readonly DayOfTheWeekFactorService _dayOfTheWeekFactorService;


        public int CalculateDiscount()
        {
            // some logic with that members
            return 0;
        }
    }
}

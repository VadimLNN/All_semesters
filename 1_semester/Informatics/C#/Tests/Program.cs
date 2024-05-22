using System;

public class MainClass
{
    public static void Main()
    {
        int[] nums = { 1, 1, 2, 2, 3 };

        int res = -1;
        if (nums.Length == 1)
            res = nums[0];
        else
        {
            for (int i = 0; i < nums.Length; i += 2)
            {
                if (i == nums.Length - 1)
                    res = nums[i];
                else if (nums[i] != nums[i + 1])
                {
                    res = nums[i];
                    break;
                }
            }
        }
            

        Console.WriteLine(res);

        Console.ReadKey();
    }
}
import java.util.*;
public class Main{
  public static void main(String[] arg)
  {
    Scanner scan = new Scanner(System.in);
    int len = scan.nextInt();
    String s1 = scan.next();
    String s2 = scan.next();
    int flag = 0,cnt = 0;;
    StringBuffer sb = new StringBuffer(s2);
    for(int i =0;i<s1.length();i++)
    {
              flag =0;

      for(int j = 0;j<sb.length();j++)
      {
   		  if(s1.charAt(i) == sb.charAt(j))
     	{
     		 sb.deleteCharAt(j); 
            flag =1;
            break;
         }
      }
     if(flag==0){
       cnt = s1.length()-i;
       break;
     }
       
    }
   System.out.println(cnt);
  }
}
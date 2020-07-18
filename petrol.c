#include <stdio.h>
int main(void) {
    int n=0, x, i, j, sum = 0;
    int ar[51];
    while((scanf("%d",&x))!=-1)
    {
        ar[n++]=x;
        sum += x;
    }
    int dp[n+1][sum+1];
    for(i=0 ; i<=n ; ++i)
        dp[i][0] = 1;
    for(i=1 ; i<=sum ; ++i)
        dp[0][i] = 0;

    for(i=1 ; i<=n ; ++i)
        for(j=1 ; j<=sum ; ++j)
        {
            dp[i][j] = dp[i-1][j];

            if(ar[i-1] <= j)
                dp[i][j] = dp[i][j] | dp[i-1][j - ar[i-1]];
        }
    int ans = sum;
    for(i=sum/2 ; i>=0 ; --i)
        if(dp[n][i])
        {
            ans = sum - i;
            break;
        }
    printf("%d",ans);
return 0;
}
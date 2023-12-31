#import "Employee.h"
#import "stdio.h"
@implementation Employee
- init: (int)eid
{
 hireDate = [[Date alloc] init];
 [hireDate setDate: hire_date_from_DB(eid)];
 return self;
}
- (int) empId
{
 return empId;
}
- (int) lengthOfService: date
{
 if( [hireDate isBefore: date] )
 return 0;
 else
 return [hireDate differenceInDays: date];
}
-(void) printName
{
 printf("%s, %s
", lName, fName);
}
@end
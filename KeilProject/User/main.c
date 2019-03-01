#include "IndicatorLight.h"
#include "SysTick.h"
#include "usart.h"
#include "usart3.h"
#include "iic.h"
#include "oled.h"
#include "adc.h"


void All_Init()
{

    LED_Init();
    SysTick_Init(72);
    USART1_Init(57600);
	USART3_Init(9600);
    IIC_Init();
	OLED_Init();
	ADCx_Init();
}

int main()
{
    int i=0;
	extern const unsigned char BMP1[];
	unsigned char str1[]="12/01/19 13:19";
	unsigned char str2[]="no GPS!";
    All_Init();
	OLED_CLS();
	
    while(1)
    {
		led = ~led;
		delay_ms(200);
		printf("adc value: %d \r\n",Get_ADC_Value(6,10));
    }

}

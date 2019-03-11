#include "adc.h"
#include "SysTick.h"
#include "usart1.h"

uint8_t ADC_QUEUE_BUF[ADC_MAX_QUEUE_BUF_SIZE];//ADC串口缓冲区
uint8_t ADC_QUEUE_REAR=0;//串口缓冲区队列尾，入队位置
uint8_t ADC_QUEUE_FRONT=0;//串口缓冲区队列首，出队位置

/*******************************************************************************
* 函 数 名         : ADCx_Init
* 函数功能		   : ADC初始化
* 输    入         : 无
* 输    出         : 无
*******************************************************************************/
void ADCx_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure; //定义结构体变量
    ADC_InitTypeDef       ADC_InitStructure;

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA|RCC_APB2Periph_ADC1,ENABLE);

    RCC_ADCCLKConfig(RCC_PCLK2_Div6);//设置ADC分频因子6 72M/6=12,ADC最大时间不能超过14M

    GPIO_InitStructure.GPIO_Pin=GPIO_Pin_6;//ADC
    GPIO_InitStructure.GPIO_Mode=GPIO_Mode_AIN;	//模拟输入
    GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
    GPIO_Init(GPIOA,&GPIO_InitStructure);

    ADC_InitStructure.ADC_Mode = ADC_Mode_Independent;
    ADC_InitStructure.ADC_ScanConvMode = DISABLE;//非扫描模式
    ADC_InitStructure.ADC_ContinuousConvMode = DISABLE;//关闭连续转换
    ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;//禁止触发检测，使用软件触发
    ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;//右对齐
    ADC_InitStructure.ADC_NbrOfChannel = 1;//1个转换在规则序列中 也就是只转换规则序列1
    ADC_Init(ADC1, &ADC_InitStructure);//ADC初始化

    ADC_Cmd(ADC1, ENABLE);//开启AD转换器

    ADC_ResetCalibration(ADC1);//重置指定的ADC的校准寄存器
    while(ADC_GetResetCalibrationStatus(ADC1));//获取ADC重置校准寄存器的状态

    ADC_StartCalibration(ADC1);//开始指定ADC的校准状态
    while(ADC_GetCalibrationStatus(ADC1));//获取指定ADC的校准程序

    ADC_SoftwareStartConvCmd(ADC1, ENABLE);//使能或者失能指定的ADC的软件转换启动功能
}

/*******************************************************************************
* 函 数 名         : Get_ADC_Value
* 函数功能		   : 获取通道ch的转换值，取times次,然后平均
* 输    入         : ch:通道编号
					 times:获取次数
* 输    出         : 通道ch的times次转换结果平均值
*******************************************************************************/
u16 Get_ADC_Value(u8 ch)
{
    //设置指定ADC的规则组通道，一个序列，采样时间
    ADC_RegularChannelConfig(ADC1, ch, 1, ADC_SampleTime_239Cycles5);	//ADC1,ADC通道,239.5个周期,提高采样时间可以提高精确度

    ADC_SoftwareStartConvCmd(ADC1, ENABLE);//使能指定的ADC1的软件转换启动功能
    while(!ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC ));//等待转换结束
    return ADC_GetConversionValue(ADC1);
}





/**
  * @brief :判断ADC串口缓冲区是否满
  * @param :void
  * @retval :返回1:满 返回0:非满
  * @usage:if(ADC_QUEUE_FULL()==1)...	if(ADC_QUEUE_FULL()==0)...
  */
uint8_t  ADC_QUEUE_FULL(void)
{
    return (uint8_t)(((ADC_QUEUE_REAR+1)% ADC_MAX_QUEUE_BUF_SIZE)==ADC_QUEUE_FRONT);
}


/**
  * @brief	:判断ADC串口缓冲区是否空
  * @param	:void
  * @retval	:返回1:空 返回0:非空
  * @usage	:if(ADC_QUEUE_EMPTY()==1)...	if(ADC_QUEUE_EMPTY()==0)...
  */
uint8_t ADC_QUEUE_EMPTY(void)
{
    return (uint8_t)(ADC_QUEUE_REAR==ADC_QUEUE_FRONT);
}

/**
  * @brief	:往ADC串口缓冲区内存入一个字节数据
  * @param	ch: uint8_t类型，写入ch
  * @retval	:1,队列满，写入失败；0，写入成功
  * @usage	:ADC_PUSH_QUEUE(0x3f)
  */
uint8_t ADC_PUSH_QUEUE(uint8_t ch)
{
    if(ADC_QUEUE_FULL())
    {
//        printf("queue full!\n");
        return 1;
    }
    ADC_QUEUE_REAR=(ADC_QUEUE_REAR+1) % ADC_MAX_QUEUE_BUF_SIZE;
    ADC_QUEUE_BUF[ADC_QUEUE_REAR]=ch;
    return 0;
}
/**
  * @brief	:从ADC串口缓冲区取出一个字节数据
  * @param	:void
  * @retval	:uint8_t 类型，即为从缓冲区取出的字节
  * @usage	:uint8_t temp;
  * @usage	:temp=ADC_POP_QUEUE();
  */
uint8_t ADC_POP_QUEUE(void)
{
    uint8_t temp;
    if(ADC_QUEUE_EMPTY())
    {
//        printf("queue empty!\n");
        return 1;
    }
    ADC_QUEUE_FRONT = (ADC_QUEUE_FRONT+1)%ADC_MAX_QUEUE_BUF_SIZE;
    temp = ADC_QUEUE_BUF[ADC_QUEUE_FRONT];
    return temp;
}

/**
  * @brief	:清空ADC串口缓冲区
  * @param	:void
  * @retval	:void
  * @usage	:ADC_CLEAR_QUEUE();
  */
void ADC_CLEAR_QUEUE(void)
{
	ADC_QUEUE_REAR=0;
	ADC_QUEUE_FRONT=0;
}

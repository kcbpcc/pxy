from telsumrypxy import check_and_send_summary

telegram_message = (
    f"    🚀 *PXY® Score Board* 🚀\n\n"
    f"💰*Daily Delta:* {delta_day:,.2f}\n\n"
    f"💰*Month Delta:* {delta_month:,.2f}\n\n"   
    f"    🔗 [PXY® Dash Board](https://console.zerodha.com/verified/0aec4aa4)"
)

# Send the summary
check_and_send_summary(telegram_message, 'vlpxy')

"""
ATM Logic Layer - Business logic for ATM operations.
Handles PIN verification, withdrawals, balance checks, and voice instructions.
"""

class ATMLogic:
    """Business logic for ATM operations."""
    
    def __init__(self, database):
        self.db = database
    
    def verify_pin(self, account_number, pin):
        """Verify user PIN."""
        return self.db.verify_pin(account_number, pin)
    
    def get_balance(self, account_number):
        """Get account balance."""
        return self.db.get_balance(account_number)
    
    def withdraw(self, account_number, amount):
        """
        Process withdrawal request.
        Returns dict with success status and new balance or error message.
        """
        current_balance = self.get_balance(account_number)
        
        if current_balance is None:
            return {'success': False, 'message': 'Account not found'}
        
        if amount > current_balance:
            return {'success': False, 'message': 'Insufficient funds'}
        
        if amount <= 0:
            return {'success': False, 'message': 'Invalid amount'}
        
        new_balance = current_balance - amount
        self.db.update_balance(account_number, new_balance)
        
        return {
            'success': True,
            'new_balance': new_balance,
            'message': 'Withdrawal successful'
        }
    
    def get_all_steps(self, action, language='en'):
        """
        Get all steps for an action in the selected language.
        Returns a list of all instructions.
        """
        instructions = self._get_instructions_dict()
        lang_instructions = instructions.get(language, instructions['en'])
        action_instructions = lang_instructions.get(action, {})
        
        # Return all steps as a list
        all_steps = []
        step_num = 1
        while step_num in action_instructions:
            all_steps.append(action_instructions[step_num])
            step_num += 1
        
        return all_steps
    
    def _get_instructions_dict(self):
        """Get the instructions dictionary."""
        return {
            'en': {
                'enter_pin': {
                    1: "Please enter your PIN using the keypad.",
                    2: "Press the confirm button after entering your PIN."
                },
                'select_action': {
                    1: "Please select an action. For withdraw cash, click the first button. For check balance, click the second button."
                },
                'withdraw': {
                    1: "You selected withdraw cash. Please enter the amount you wish to withdraw.",
                    2: "Confirm the amount on the screen.",
                    3: "Please collect your cash from the dispenser.",
                    4: "Transaction complete. Thank you for using our ATM."
                },
                'check_balance': {
                    1: "You selected check balance. Your current balance is displayed on the screen.",
                    2: "Transaction complete. Thank you."
                }
            },
            'ur': {  # Urdu
                'select_action': {
                    1: "براہ کرم ایک عمل منتخب کریں۔ نقدی نکالنے کے لیے پہلا بٹن دبائیں۔ بیلنس چیک کرنے کے لیے دوسرا بٹن دبائیں۔"
                },
                'withdraw': {
                    1: "آپ نے نقدی نکالنے کا انتخاب کیا۔ براہ کرم وہ رقم درج کریں جو آپ نکالنا چاہتے ہیں۔",
                    2: "اسکرین پر رقم کی تصدیق کریں۔",
                    3: "براہ کرم ڈسپنسر سے اپنی نقدی وصول کریں۔",
                    4: "لین دین مکمل ہو گیا۔ ہمارے اے ٹی ایم استعمال کرنے کا شکریہ۔"
                },
                'check_balance': {
                    1: "آپ نے بیلنس چیک کا انتخاب کیا۔ آپ کا موجودہ بیلنس اسکرین پر دکھایا گیا ہے۔",
                    2: "لین دین مکمل ہو گیا۔ شکریہ۔"
                },
                'enter_pin': {
                    1: "براہ کرم کی پیڈ استعمال کرتے ہوئے اپنا PIN درج کریں۔",
                    2: "PIN درج کرنے کے بعد تصدیق کا بٹن دبائیں۔"
                }
            },
            'pa': {  # Pakistani Punjabi (Shahmukhi - Urdu Script)
                'select_action': {
                    1: "براہ کرم ایک عمل منتخب کریں۔ نقدی نکالنے کے لیے پہلا بٹن دبائیں۔ بیلنس چیک کرنے کے لیے دوسرا بٹن دبائیں۔"
                },
                'withdraw': {
                    1: "آپ نے نقدی نکالنے کا انتخاب کیا۔ براہ کرم وہ رقم درج کریں جو آپ نکالنا چاہتے ہیں۔",
                    2: "اسکرین پر رقم کی تصدیق کریں۔",
                    3: "براہ کرم ڈسپنسر سے اپنی نقدی وصول کریں۔",
                    4: "لین دین مکمل ہو گیا۔ ہمارے اے ٹی ایم استعمال کرنے کا شکریہ۔"
                },
                'check_balance': {
                    1: "آپ نے بیلنس چیک کا انتخاب کیا۔ آپ کا موجودہ بیلنس اسکرین پر دکھایا گیا ہے۔",
                    2: "لین دین مکمل ہو گیا۔ شکریہ۔"
                },
                'enter_pin': {
                    1: "ਕਿਰਪਾ ਕਰਕੇ ਕੀਪੈਡ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਆਪਣਾ PIN ਦਰਜ ਕਰੋ।",
                    2: "PIN ਦਰਜ ਕਰਨ ਤੋਂ ਬਾਅਦ ਪੁਸ਼ਟੀ ਬਟਨ ਦਬਾਓ।"
                }
            },
            'ps': {  # Pashto
                'select_action': {
                    1: "مهرباني وکړئ یو عمل وټاکئ. د نغدو پیسو وایستلو لپاره، لومړۍ تڼۍ فشار ورکړئ. د بیلانس چیک کولو لپاره، دویمه تڼۍ فشار ورکړئ."
                },
                'withdraw': {
                    1: "تاسو د نغدو پیسو وایستلو انتخاب کړی. مهرباني وکړئ هغه پیسې ولیکئ چې تاسو یې وایستل غواړئ.",
                    2: "په سکرین کې د پیسو تصدیق وکړئ.",
                    3: "مهرباني وکړئ خپلې نغدې پیسې د ویشونکي څخه واخلئ.",
                    4: "معامله بشپړه شوه. زموږ ATM کارولو لپاره مننه."
                },
                'check_balance': {
                    1: "تاسو د بیلانس چیک انتخاب کړی. ستاسو اوسنی بیلانس په سکرین کې ښودل شوی.",
                    2: "معامله بشپړه شوه. مننه."
                },
                'enter_pin': {
                    1: "مهرباني وکړئ د کی پیډ کارولو سره خپل PIN ولیکئ.",
                    2: "د PIN لیکلو وروسته د تصدیق تڼۍ فشار ورکړئ."
                }
            },
            'sd': {  # Sindhi
                'select_action': {
                    1: "مهرباني ڪري هڪ عمل چونڊيو. نقدي نڪتل ڪرڻ لاءِ، پهرين بٽڻ دٻايو. بيلنس چيڪ ڪرڻ لاءِ، ٻيون بٽڻ دٻايو."
                },
                'withdraw': {
                    1: "توهان نقدي نڪتل ڪرڻ جو انتخاب ڪيو. مهرباني ڪري اهو رقم داخل ڪريو جيڪو توهان نڪتل ڪرڻ چاهيو ٿا.",
                    2: "اسڪرين تي رقم جي تصديق ڪريو.",
                    3: "مهرباني ڪري ڊسپينسر کان پنهنجو نقد وصول ڪريو.",
                    4: "لين ڏيڻ مڪمل ٿي ويو. اسان جي ATM استعمال ڪرڻ لاءِ مهرباني."
                },
                'check_balance': {
                    1: "توهان بيلنس چيڪ جو انتخاب ڪيو. توهان جو موجوده بيلنس اسڪرين تي ڏيکاريو ويو آهي.",
                    2: "لين ڏيڻ مڪمل ٿي ويو. مهرباني."
                },
                'enter_pin': {
                    1: "مهرباني ڪري ڪي پيڊ استعمال ڪندي پنهنجو PIN داخل ڪريو.",
                    2: "PIN داخل ڪرڻ کان پوءِ تصديق بٽڻ دٻايو."
                }
            },
            'ar': {  # Arabic
                'select_action': {
                    1: "يرجى اختيار إجراء. لسحب النقد، اضغط على الزر الأول. للتحقق من الرصيد، اضغط على الزر الثاني."
                },
                'withdraw': {
                    1: "لقد اخترت سحب النقد. يرجى إدخال المبلغ الذي ترغب في سحبه.",
                    2: "قم بتأكيد المبلغ على الشاشة.",
                    3: "يرجى جمع النقد من الموزع.",
                    4: "اكتملت المعاملة. شكرًا لاستخدام أجهزة الصراف الآلي لدينا."
                },
                'check_balance': {
                    1: "لقد اخترت التحقق من الرصيد. يتم عرض رصيدك الحالي على الشاشة.",
                    2: "اكتملت المعاملة. شكرًا لك."
                },
                'enter_pin': {
                    1: "يرجى إدخال رقم PIN الخاص بك باستخدام لوحة المفاتيح.",
                    2: "اضغط على زر التأكيد بعد إدخال رقم PIN."
                }
            }
        }
        
        lang_instructions = instructions.get(language, instructions['en'])
        action_instructions = lang_instructions.get(action, {})
        
        return action_instructions.get(step, "Please proceed with the next step.")
    
    def get_voice_instructions(self, action, language='en', step=1):
        """
        Get step-by-step voice instructions in the selected language.
        This provides text that can be converted to speech.
        """
        instructions = self._get_instructions_dict()
        lang_instructions = instructions.get(language, instructions['en'])
        action_instructions = lang_instructions.get(action, {})
        
        return action_instructions.get(step, "Please proceed with the next step.")
Usage: Put your bot's token into token.md, your ID into myAccountID.md.

Note: UTC+7 in used.

!help	

		Show this instructions.

!list, !l	

		Show schedules.

!add, !a	<content> <month>/<day> <hour>:<minute> [-w <week>] [-m <month>] [-r <alarm_before>] [-n <note>]

		Add new schedules to list.
       
        <content> <day>/<month> <hour>:<minute> [-w <week>] [-m <month>] [-r <alarm_before>] [-n <note>]

        Compulsory:
            content         Alarm for?
            month/day       On day ?
            hour:minutes    When ? (24-hour format)

        Optional:
            -w week             repeat in next n (int) weeks. Default is 0.
            -m month            repeat in next n (int) months. Default is 0.

            CAUTION: Only week or month. If both is exist, bot use week first.

            -b before           ring before n (int) minutes. Default is 5.
            -n note             note for this shedule

        Example:
            !add test 30/4 11:30 -w 1 -m 2 -b 3 -n abcxyz

!remove, !rm	<order>

		Remove a schedule from list.
        CAUTION: CANNOT UNDO.
        
        !rm <order> / <all>

!setup, !s	<order> [-w <week>] [-m <month>] [-r <alarm_before>] [-n <note>]

		Change optional setting for ordered schedule.
        
        Compulsory:
            order               Which is the order need to repair?

        Optional:
            -w week             repeat per week in n (int) weeks. Default is 0.
            -m month            repeat per month in n (int) months. Default is 0.
            -b before           ring before n (int) minutes. Default is 5.
            -n note             note for this shedule

        Example:
            !s 0 -w 1 -m 2 -r 3 -n abcxyz
	    
!time

		Show current time.


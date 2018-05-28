Receive_Data()

Verify_Data()

a=test()

if a=="Y":
	b=Transform(a)

	if b>1:
		Load()

	c=select1()

	if c==5:
		e=select2(c)

		if e>=5:
			d=select4(c)

			if d<=8:
				runit()

	if c==2:
		d=select3(c)

		if d>8:
			runit()

		if d<=8:
			runit()

if a=="N":
	Report_Errors()


key = str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-=!@#$%^&*()_+", "w4hZ&pvI*-#ko)_AgNT3^tr9XB=czWyF0OLQmsiDx5Y$qb6GKeJU(M27ECVu%nPH1+l@d8R!jaSf")
reversekey = str.maketrans("w4hZ&pvI*-#ko)_AgNT3^tr9XB=czWyF0OLQmsiDx5Y$qb6GKeJU(M27ECVu%nPH1+l@d8R!jaSf", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-=!@#$%^&*()_+")

def decrypt(outpt):
	return outpt.translate(reversekey)



#print(decrypt("rN_)vwNwv&n%CC"))
#print(decrypt("^*6)IX=L6J)h7d!WF@d!VCJFOcyq8RFKp"))

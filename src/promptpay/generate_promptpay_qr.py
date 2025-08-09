import qrcode
import crcmod

def generate_promptpay_payload(phone_number: str, amount: float) -> str:
    # แปลงเบอร์โทรเป็นรูปแบบ EMVCo
    if phone_number.startswith("0"):
        phone_number = "66" + phone_number[1:]
    phone_number = phone_number.zfill(13)

    payload = (
        "000201"  # Payload Format Indicator
        "010212"  # Point of Initiation Method (12 = Static)
        "29370016A000000677010111"  # Merchant Account Info Template
        "01130066" + phone_number +  # Mobile number
        "5303764"  # Currency code (764 = THB)
        f"5405{int(amount * 100):05d}"  # Amount
        "5802TH"  # Country Code
        "6304"  # CRC will be added later
    )

    # คำนวณ CRC16-CCITT
    crc16 = crcmod.predefined.mkCrcFun('crc-ccitt-false')
    checksum = format(crc16(payload.encode('ascii')), '04X')

    return payload + checksum

def generate_promptpay_qr(phone_number: str, amount: float, filename: str):
    payload = generate_promptpay_payload(phone_number, amount)
    img = qrcode.make(payload)
    img.save(filename)
    print(f"✅ QR Code saved to {filename}")

# ตัวอย่างการใช้งาน:
if __name__ == "__main__":
    # เปลี่ยนเบอร์และยอดเงินตามต้องการ
    generate_promptpay_qr("0881234567", 20.00, "promptpay_qr_20baht.png")

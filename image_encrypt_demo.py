import numpy as np
from PIL import Image
import os


# =========================
# 1. 工具函数：读取与保存灰度图像
# =========================
def load_gray_image(path: str) -> np.ndarray:
    """
    读取一张本地灰度图像，返回像素矩阵（uint8）
    """
    img = Image.open(path).convert("L")  # 转为灰度图（L 模式）
    arr = np.array(img, dtype=np.uint8)
    return arr


def save_gray_image(arr: np.ndarray, path: str):
    """
    将像素矩阵保存为灰度图像
    """
    img = Image.fromarray(arr.astype(np.uint8), mode="L")
    img.save(path)


# =========================
# 2. 生成密钥 & 图像加解密
# =========================
def generate_key_matrix(shape) -> np.ndarray:
    """
    生成与图像同尺寸的随机密钥矩阵（0~255）
    """
    key = np.random.randint(0, 256, size=shape, dtype=np.uint8)
    return key


def encrypt_image(image_arr: np.ndarray, key_arr: np.ndarray) -> np.ndarray:
    """
    使用简单 XOR 对图像进行加密：
    密文 = 原图像素 ^ 密钥
    """
    cipher = np.bitwise_xor(image_arr, key_arr)
    return cipher


def decrypt_image(cipher_arr: np.ndarray, key_arr: np.ndarray) -> np.ndarray:
    """
    使用相同的密钥进行解密：
    明文 = 密文 ^ 密钥
    （XOR 的逆运算就是自身）
    """
    plain = np.bitwise_xor(cipher_arr, key_arr)
    return plain


# =========================
# 3. 在密文状态下进行运算示例
# =========================
def ciphertext_statistics(cipher_arr: np.ndarray):
    """
    对密文图像做简单统计测量（例：平均值、方差）
    这里只是演示“在密文状态下运算”的概念
    """
    mean_val = float(np.mean(cipher_arr))
    var_val = float(np.var(cipher_arr))
    return mean_val, var_val


def xor_two_cipher_images(cipher_arr1: np.ndarray, cipher_arr2: np.ndarray) -> np.ndarray:
    """
    对两幅密文图像做像素级 XOR 运算
    注意：这里只是演示操作过程，不保证有特殊的密码学意义
    """
    # 取两张图像的公共尺寸
    h = min(cipher_arr1.shape[0], cipher_arr2.shape[0])
    w = min(cipher_arr1.shape[1], cipher_arr2.shape[1])

    sub1 = cipher_arr1[:h, :w]
    sub2 = cipher_arr2[:h, :w]

    result = np.bitwise_xor(sub1, sub2)
    return result


# =========================
# 4. 主流程示例
# =========================
def main():
    # ==== 0. 设置输入输出路径 ====
    # 请将 'input1.png' 换成你自己的灰度图像文件名
    input_image_path1 = "Couple.tif"
    input_image_path2 = "boat.tiff"  # 第二张图像，用来演示密文 XOR 运算，可选

    output_dir = "output_images"
    os.makedirs(output_dir, exist_ok=True)

    # ==== 1. 读取原始灰度图像 ====
    img_arr1 = load_gray_image(input_image_path1)
    print("原始图像1尺寸：", img_arr1.shape)

    # 可选：若存在第二张图像，则读取
    if os.path.exists(input_image_path2):
        img_arr2 = load_gray_image(input_image_path2)
        print("原始图像2尺寸：", img_arr2.shape)
    else:
        img_arr2 = None
        print("未找到第二张图像，只进行单图像加密演示。")

    # ==== 2. 生成与图像同尺寸的密钥矩阵 ====
    key_arr1 = generate_key_matrix(img_arr1.shape)

    # ==== 3. 对图像进行加密 ====
    cipher_arr1 = encrypt_image(img_arr1, key_arr1)
    save_gray_image(cipher_arr1, os.path.join(output_dir, "cipher_image1.png"))
    print("图像1加密完成，已保存为 cipher_image1.png")

    # ==== 4. 在密文状态下计算统计量 ====
    mean_val, var_val = ciphertext_statistics(cipher_arr1)
    print("密文图像1的平均值：", mean_val)
    print("密文图像1的方差：", var_val)

    # ==== 5. 使用同一密钥进行解密 ====
    decrypted_arr1 = decrypt_image(cipher_arr1, key_arr1)
    save_gray_image(decrypted_arr1, os.path.join(output_dir, "decrypted_image1.png"))
    print("图像1解密完成，已保存为 decrypted_image1.png")

    # ==== 6. 验证解密后与原图是否一致 ====
    is_same = np.array_equal(img_arr1, decrypted_arr1)
    print("解密后图像是否与原图完全相同：", is_same)

    # ==== 7. （可选）对两幅密文图像进行像素级 XOR 运算 ====
    if img_arr2 is not None:
        # 为第二张图像也生成一份密钥，并加密
        key_arr2 = generate_key_matrix(img_arr2.shape)
        cipher_arr2 = encrypt_image(img_arr2, key_arr2)
        save_gray_image(cipher_arr2, os.path.join(output_dir, "cipher_image2.png"))
        print("图像2加密完成，已保存为 cipher_image2.png")

        # 对两幅密文图像做 XOR 运算（演示“密文域运算”）
        xor_cipher = xor_two_cipher_images(cipher_arr1, cipher_arr2)
        save_gray_image(xor_cipher, os.path.join(output_dir, "cipher_xor.png"))
        print("两幅密文图像 XOR 运算结果已保存为 cipher_xor.png")


if __name__ == "__main__":
    main()

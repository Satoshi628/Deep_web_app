#coding: utf-8
#----- 標準ライブラリ -----#
# None

#----- 専用ライブラリ -----#
import streamlit as st
import requests
from Multi_App import MultiApp
from PIL import Image
from deep_AI import deep_ai_func
#----- 自作モジュール -----#
# None


@st.cache
def image_load(image):
    img = Image.open(image)
    return img


@st.cache
def Deep_AI_load(**kwargs):
    img = deep_ai_func(**kwargs)
    return img

#1つの関数で使うst.session_stateは
#image_file,input_image,output_imageの3つ(Similarityは5つ)


def Deep_Dream():
    #レイアウト
    st.title("Deep Dream")
    """
        ###### このAIは画像に民族的な特徴を付与します. 詳細はサンプル画像を御覧ください.
        ### 変換したい画像をアップロードしてください
    """
    
    # typeがNoneだとすべての拡張子が許される。
    st.session_state.Deep_Dream_image_file = st.file_uploader("File Upload", type=None, key="Dream")
    Run_botton = st.button('Run')

    #画像が入力されていなかった時のサンプル画像
    if "Deep_Dream_input_image" not in st.session_state:
        st.session_state.Deep_Dream_input_image = image_load("Sample_image/Deep_Dream1.jpg")
    if "Deep_Dream_output_image" not in st.session_state:
        st.session_state.Deep_Dream_output_image = image_load("Sample_image/Deep_Dream2.png")

    ##処理部分##

    #ファイルがアップロードされたら
    if st.session_state.Deep_Dream_image_file:
        st.session_state.Deep_Dream_input_image = image_load(st.session_state.Deep_Dream_image_file)
    else:  #アップロードされていないなら
        #サンプル画像に変える
        st.session_state.Deep_Dream_input_image = image_load("Sample_image/Deep_Dream1.jpg")
        st.session_state.Deep_Dream_output_image = image_load("Sample_image/Deep_Dream2.png")

    #Runボタンが押されたら
    if Run_botton:
        if st.session_state.Deep_Dream_image_file:
            st.session_state.Deep_Dream_output_image = Deep_AI_load(AI_key="Dream", image=st.session_state.Deep_Dream_image_file.getvalue())
            if st.session_state.Deep_Dream_output_image is None:  # 正しく出力出来なかった場合
                """
                    ##### ファイルの出力に失敗しました.
                """
                st.session_state.Deep_Dream_output_image = image_load(
                    "Sample_image/Deep_Dream2.png")
        else:
            """
                ##### 画像を入力してください.
            """

    if isinstance(st.session_state.Deep_Dream_output_image, bytes):
        extension = st.radio("Select the extension to Download",
                            ['png', 'jpeg'])
        st.download_button(
            label="Download Output Image",
            data=st.session_state.Deep_Dream_output_image,
            file_name='output_image.{}'.format(extension),
            mime="image/{}".format(extension)
        )

    #画像は2列で表示する
    col1, col2 = st.columns(2)

    # 入力画像表示
    with col1:
        st.image(
            st.session_state.Deep_Dream_input_image, caption="入力画像",
            use_column_width=True
        )
    
    # 出力画像表示
    with col2:
        st.image(
            st.session_state.Deep_Dream_output_image, caption="出力画像",
            use_column_width=True
        )


def Similarity():
    #レイアウト
    st.title("Similarity")
    """
        ###### このAIは2つの画像の類似度を計算します.
        ### 変換したい画像をアップロードしてください
    """
    # typeがNoneだとすべての拡張子が許される。
    st.session_state.Similarity_image_file1 = st.file_uploader("File Upload", type=None, key="Similarity1")
    st.session_state.Similarity_image_file2 = st.file_uploader("File Upload", type=None, key="Similarity2")
    Run_botton = st.button('Run')

    #画像が入力されていなかった時のサンプル画像
    if "Similarity_input_image" not in st.session_state:
        st.session_state.Similarity_input_image1 = image_load("Sample_image/Similarity1.jpg")
    if "Similarity_input_image" not in st.session_state:
        st.session_state.Similarity_input_image2 = image_load("Sample_image/Similarity2.jpg")
    if "Similarity_output_similar" not in st.session_state:
        st.session_state.Similarity_output_similar = 30

    ##処理部分##

    #ファイル1がアップロードされたら
    if st.session_state.Similarity_image_file1:
        st.session_state.Similarity_input_image1 = image_load(st.session_state.Similarity_image_file1)
    else:  #アップロードされていないなら
        #サンプル画像に変える
        st.session_state.Similarity_input_image1 = image_load("Sample_image/Similarity1.jpg")
    
    #ファイル2がアップロードされたら
    if st.session_state.Similarity_image_file2:
        st.session_state.Similarity_input_image2 = image_load(st.session_state.Similarity_image_file2)
    else:  #アップロードされていないなら
        #サンプル画像に変える
        st.session_state.Similarity_input_image2 = image_load("Sample_image/Similarity2.jpg")

    #Runボタンが押されたら
    if Run_botton:
        #入力画像があるのなら
        if st.session_state.Similarity_image_file1 and st.session_state.Similarity_image_file2:
            st.session_state.Similarity_output_similar = Deep_AI_load(AI_key="Similarity",
                image1=st.session_state.Similarity_image_file1.getvalue(),
                image2=st.session_state.Similarity_image_file2.getvalue())
            
            if st.session_state.Similarity_output_similar is None:  # 正しく出力出来なかった場合
                """
                    ##### ファイルの出力に失敗しました.
                """
                st.session_state.Similarity_output_similar = 30
        else:
            """
                #### Please enter two image.
            """
    
    st.text("類似度距離:{}".format(st.session_state.Similarity_output_similar))
    st.text("0~19:とても似ている    20~24:似ている  25~29:あまり似ていない    30~:別物")
    #画像は2列で表示する
    col1, col2 = st.columns(2)

    # 入力画像表示
    with col1:
        st.image(
            st.session_state.Similarity_input_image1, caption="入力画像1",
            use_column_width=True
        )
    
    # 出力画像表示
    with col2:
        st.image(
            st.session_state.Similarity_input_image2, caption="入力画像2",
            use_column_width=True
        )


def Colorization():
    #レイアウト
    st.title("Colorization")
    """
        ###### このAIはモノクロ画像をカラー画像に変換します.
        ### 変換したい画像をアップロードしてください
    """
    # typeがNoneだとすべての拡張子が許される。
    st.session_state.Colorization_image_file = st.file_uploader("File Upload", type=None, key="Color")
    Run_botton = st.button('Run')

    #画像が入力されていなかった時のサンプル画像
    if "Colorization_input_image" not in st.session_state:
        st.session_state.Colorization_input_image = image_load("Sample_image/Colorization1.jpg")
    if "Colorization_output_image" not in st.session_state:
        st.session_state.Colorization_output_image = image_load("Sample_image/Colorization2.png")

    ##処理部分##

    #ファイルがアップロードされたら
    if st.session_state.Colorization_image_file:
        st.session_state.Colorization_input_image = image_load(st.session_state.Colorization_image_file)
    else:  #アップロードされていないなら
        #サンプル画像に変える
        st.session_state.Colorization_input_image = image_load("Sample_image/Colorization1.jpg")
        st.session_state.Colorization_output_image = image_load("Sample_image/Colorization2.png")

    #Runボタンが押されたら
    if Run_botton:
        if st.session_state.Colorization_image_file:
            st.session_state.Colorization_output_image = Deep_AI_load(AI_key="Color", image=st.session_state.Colorization_image_file.getvalue())
            if st.session_state.Colorization_output_image is None:  # 正しく出力出来なかった場合
                """
                    ##### ファイルの出力に失敗しました.
                """
                st.session_state.Colorization_output_image = image_load("Sample_image/Colorization2.png")
        else:
            """
                ##### 画像を入力してください.
            """

    if isinstance(st.session_state.Colorization_output_image, bytes):
        extension = st.radio("Select the extension to Download",
                            ['png', 'jpeg'])
        st.download_button(
            label="Download Output Image",
            data=st.session_state.Colorization_output_image,
            file_name='output_image.{}'.format(extension),
            mime="image/{}".format(extension)
        )

    #画像は2列で表示する
    col1, col2 = st.columns(2)

    # 入力画像表示
    with col1:
        st.image(
            st.session_state.Colorization_input_image, caption="入力画像",
            use_column_width=True
        )
    
    # 出力画像表示
    with col2:
        st.image(
            st.session_state.Colorization_output_image, caption="出力画像",
            use_column_width=True
        )


def High_Resolution():
    #レイアウト
    st.title("High_Resolution")
    """
        ###### このAIは画像を高解像度画像に変換します. 
        ###### 入力画像のサイズに応じて実行時間が長くなります. 注意してください.  
        ### 変換したい画像をアップロードしてください
    """
    # typeがNoneだとすべての拡張子が許される。
    st.session_state.High_Resolutionimage_file = st.file_uploader("File Upload", type=None, key="Resolution")
    Run_botton = st.button('Run')

    #画像が入力されていなかった時のサンプル画像
    if "High_Resolution_input_image" not in st.session_state:
        st.session_state.High_Resolution_input_image = image_load("Sample_image/High_Resolution1.jpg")
    if "High_Resolution_output_image" not in st.session_state:
        st.session_state.High_Resolution_output_image = image_load("Sample_image/High_Resolution2.png")

    ##処理部分##

    #ファイルがアップロードされたら
    if st.session_state.High_Resolutionimage_file:
        st.session_state.High_Resolution_input_image = image_load(st.session_state.High_Resolutionimage_file)
    else:  #アップロードされていないなら
        #サンプル画像に変える
        st.session_state.High_Resolution_input_image = image_load("Sample_image/High_Resolution1.jpg")
        st.session_state.High_Resolution_output_image = image_load("Sample_image/High_Resolution2.png")

    #Runボタンが押されたら
    if Run_botton:
        if st.session_state.High_Resolutionimage_file:
            st.session_state.High_Resolution_output_image = Deep_AI_load(AI_key="Resolution", image=st.session_state.High_Resolutionimage_file.getvalue())
            if st.session_state.High_Resolution_output_image is None:  # 正しく出力出来なかった場合
                """
                    ##### ファイルの出力に失敗しました.
                """
                st.session_state.High_Resolution_output_image = image_load("Sample_image/High_Resolution2.png")
        else:
            """
                ##### 画像を入力してください.
            """

    if isinstance(st.session_state.High_Resolution_output_image, bytes):
        extension = st.radio("Select the extension to Download",
                            ['png', 'jpeg'])
        st.download_button(
            label="Download Output Image",
            data=st.session_state.High_Resolution_output_image,
            file_name='output_image.{}'.format(extension),
            mime="image/{}".format(extension)
        )

    #画像は2列で表示する
    col1, col2 = st.columns(2)

    # 入力画像表示
    with col1:
        st.image(
            st.session_state.High_Resolution_input_image, caption="入力画像",
            use_column_width=True
        )
    
    # 出力画像表示
    with col2:
        st.image(
            st.session_state.High_Resolution_output_image, caption="出力画像",
            use_column_width=True
        )


def Toy():
    #レイアウト
    st.title("Toy")
    """
        ###### このAIは人の顔をディズニー、ピクサー風の顔に変換します. 詳細はサンプル画像をご覧ください.
        ### 変換したい画像をアップロードしてください
    """
    # typeがNoneだとすべての拡張子が許される。
    st.session_state.Toy_image_file = st.file_uploader("File Upload", type=None, key="Toy")
    Run_botton = st.button('Run')

    #画像が入力されていなかった時のサンプル画像
    if "Toy_input_image" not in st.session_state:
        st.session_state.Toy_input_image = image_load("Sample_image/Toy1.jpg")
    if "Toy_output_image" not in st.session_state:
        st.session_state.Toy_output_image = image_load("Sample_image/Toy2.png")

    ##処理部分##

    #ファイルがアップロードされたら
    if st.session_state.Toy_image_file:
        st.session_state.Toy_input_image = image_load(st.session_state.Toy_image_file)
    else:  #アップロードされていないなら
        #サンプル画像に変える
        st.session_state.Toy_input_image = image_load("Sample_image/Toy1.jpg")
        st.session_state.Toy_output_image = image_load("Sample_image/Toy2.png")

    #Runボタンが押されたら
    if Run_botton:
        if st.session_state.Toy_image_file:
            st.session_state.Toy_output_image = Deep_AI_load(AI_key="Toy", image=st.session_state.Toy_image_file.getvalue())
            if st.session_state.Toy_output_image is None:  # 正しく出力出来なかった場合
                """
                    ##### ファイルの出力に失敗しました.
                    ##### 人の顔が含まれる画像を入力してください.
                """
                st.session_state.Toy_output_image = image_load("Sample_image/Toy2.png")
        else:
            """
                ##### 画像を入力してください.
            """

    if isinstance(st.session_state.Toy_output_image, bytes):
        extension = st.radio("Select the extension to Download",
                            ['png', 'jpeg'])
        st.download_button(
            label="Download Output Image",
            data=st.session_state.Toy_output_image,
            file_name='output_image.{}'.format(extension),
            mime="image/{}".format(extension)
        )

    #画像は2列で表示する
    col1, col2 = st.columns(2)

    # 入力画像表示
    with col1:
        st.image(
            st.session_state.Toy_input_image, caption="入力画像",
            use_column_width=True
        )
    
    # 出力画像表示
    with col2:
        st.image(
            st.session_state.Toy_output_image, caption="出力画像",
            use_column_width=True
        )


multi_page = MultiApp()
multi_page.add_app("Deep Dream", Deep_Dream)
multi_page.add_app("Similaryty", Similarity)
multi_page.add_app("Colorization", Colorization)
multi_page.add_app("High Resolution", High_Resolution)
multi_page.add_app("Toy", Toy)
multi_page.run()

# iPhone Duo 香港 Apple Store 監控工具（Windows EXE）

這個工具監測 Apple 香港官方購買頁面的 **iPhone Duo** 配置，預設為：

- 容量：256GB
- 顏色：Night Sky
- 購買頁面：`https://www.apple.com/hk/shop/buy-iphone/iphone-duo`

Apple 官方購買頁列出 iPhone Duo 的容量為 256GB、512GB、1TB 和 2TB，顏色為 Star White 及 Night Sky。產品頁面及購買頁面均顯示這是可摺疊 iPhone Duo。

## 下載及執行 EXE

GitHub Actions 完成 Windows build 後，下載 `iPhoneDuoMonitor-Windows.zip`，解壓縮後雙擊：

```text
iPhoneDuoMonitor.exe
```

程式會自動開啟 `http://127.0.0.1:5050`，並使用 Windows 內置的 Microsoft Edge 開啟 Apple 頁面。首次啟動時，請在瀏覽器內手動登入、確認資料或處理網站提示。

> 這是本機工具，不會把 Apple 登入資料傳送到其他伺服器。瀏覽器資料會保存到使用者家目錄下的 `.apple-hk-stock-profile` 資料夾。

## 本機自行打包

在 Windows PowerShell 進入此資料夾後執行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\build_windows.ps1
```

輸出檔案會位於：

```text
release\iPhoneDuoMonitor-Windows.zip
```

## 監控限制

工具只會讀取頁面、定時重新整理及提醒。它**不會**自動加入購物袋、付款、提交訂單、處理 CAPTCHA、繞過排隊或規避 Apple 的反機器人措施。看到通知後，請由你手動確認容量、顏色、配送／取貨日期及價格，再自行決定是否購買。

如果 Microsoft Edge 不可用，程式會嘗試使用 Playwright Chromium；這種後備方式可能需要額外安裝瀏覽器元件。

## 官方資料

- [Apple 香港 iPhone Duo 產品頁](https://www.apple.com/hk/en/iphone-duo/)
- [Apple 香港 iPhone Duo 購買頁](https://www.apple.com/hk/shop/buy-iphone/iphone-duo)

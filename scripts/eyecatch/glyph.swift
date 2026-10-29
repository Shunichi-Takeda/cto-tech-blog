// 文字列を、アンチエイリアス無しの1ビットの点の並びにして標準出力へ書く。
// usage: swift glyph.swift <フォント名> <ピクセルサイズ> <文字列>
import CoreGraphics
import CoreText
import Foundation

let args = CommandLine.arguments
let font = CTFontCreateWithName(args[1] as CFString, CGFloat(Double(args[2])!), nil)
let attr = NSAttributedString(string: args[3], attributes: [kCTFontAttributeName as NSAttributedString.Key: font, kCTForegroundColorFromContextAttributeName as NSAttributedString.Key: true])
let line = CTLineCreateWithAttributedString(attr)
var ascent: CGFloat = 0, descent: CGFloat = 0, leading: CGFloat = 0
let width = Int(ceil(CTLineGetTypographicBounds(line, &ascent, &descent, &leading)))
let height = Int(ceil(ascent + descent))
let ctx = CGContext(data: nil, width: width, height: height, bitsPerComponent: 8, bytesPerRow: width,
                    space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue)!
ctx.setFillColor(gray: 0, alpha: 1)
ctx.fill(CGRect(x: 0, y: 0, width: width, height: height))
ctx.setShouldAntialias(false)
ctx.setAllowsFontSmoothing(false)
ctx.setFillColor(gray: 1, alpha: 1)
ctx.textPosition = CGPoint(x: 0, y: descent)
CTLineDraw(line, ctx)
let buf = ctx.data!.assumingMemoryBound(to: UInt8.self)
for y in 0..<height {
    var row = ""
    for x in 0..<width { row += buf[y * width + x] > 127 ? "#" : "." }
    print(row)
}

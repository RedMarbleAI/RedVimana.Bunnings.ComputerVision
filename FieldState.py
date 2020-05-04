from PIL import Image, ImageDraw, ImageFont

class FieldState(object):
    def __init__(this):
        this.mPeople = []
        this.mImages = []
        return
    
    @property
    def Images(this):
        return this.mImages
    
    @Images.setter
    def Images(this, images):
        this.mImages = images
    
    @property
    def Time(this):
        return this.mTime
    
    @Time.setter
    def Time(this, time):
        this.mTime = time
        
    @property
    def People(this):
        return this.mPeople
    
    @People.setter
    def People(this, people):
        this.mPeople = people
        
    def DrawImage(this):
        boundaryWidth = 100
        boundaryHeight = 100
        
        image = this.DrawBaseImage()
        draw = ImageDraw.Draw(image)
        
        personRadius = 10
        colorPersonOutline = (0, 0, 0, 255)
        colorPersonNormalFill = (0, 255, 0, 255)
        colorPersonDangerFill = (0, 0, 255, 255)

        for i in range(len(this.People)):
            person = this.People[i]

            isInProximity = False

            for j in range(len(this.People)):
                if i != j:
                    distance = (this.People[j] - person).Length

                    if distance <= 150:
                        isInProximity = True


            topLeftX = person.X - personRadius
            topLeftY = person.Y - personRadius
            bottomRightX = person.X + personRadius
            bottomRightY = person.Y + personRadius
            
            draw.ellipse([(topLeftX, topLeftY), (bottomRightX, bottomRightY)], outline=colorPersonOutline, fill=colorPersonDangerFill if isInProximity else colorPersonNormalFill)
        
        return image
    
    def DrawBaseImage(this):
        shelfWidth = 620
        shelfHeight = 110
        backPassageWidth = 145
        frontAreaWidth = 285
        boundaryWidth = 100
        boundaryHeight = 100
        intershelfSpacingHeight = 165
        counterWidth = 120
        counterHeight = 490

        floorWidth = (2 * boundaryWidth) + backPassageWidth + (2 * shelfWidth) + frontAreaWidth
        floorHeight = (2 * boundaryHeight) + (5 * intershelfSpacingHeight) + (4 * shelfHeight)

        colorBackground = (255, 255, 255, 255)
        colorBoundary = (128, 128, 128, 128)
        colorShelves = (128, 128, 128, 255)
        colorTextShelves = (0, 0, 0, 255)
        colorCounter = (128, 128, 128, 255)
        colorTextCounter = (0, 0, 0, 255)

        textFont = ImageFont.truetype("arial.ttf", 28, encoding="unic")

        image = Image.new("RGBA", (floorWidth, floorHeight), colorBackground)
        draw = ImageDraw.Draw(image)


        # Boundaries
        draw.rectangle([(0, 0), (floorWidth, boundaryHeight)], fill=colorBoundary)
        draw.rectangle([(0, 0), (boundaryWidth, floorHeight)], fill=colorBoundary)
        draw.rectangle([(0, floorHeight - boundaryHeight), (floorWidth, floorHeight)], fill=colorBoundary)
        draw.rectangle([(floorWidth - boundaryWidth, 0), (floorWidth, floorHeight)], fill=colorBoundary)

        #Shelves
        draw.rectangle([(245, 265), (1485, 375)], outline=colorShelves, width=3)
        draw.line([(865, 265), (865, 375)], fill=colorShelves, width=3)
        draw.text((500, 310), u"Shelf 3m", colorTextShelves, textFont)
        draw.text((1100, 310), u"Shelf 1.5m", colorTextShelves, textFont)
        draw.rectangle([(245, 540), (1485, 650)], outline=colorShelves, width=3)
        draw.line([(865, 540), (865, 650)], fill=colorShelves, width=3)
        draw.text((500, 585), u"Shelf 3m", colorTextShelves, textFont)
        draw.text((1100, 585), u"Shelf 1.5m", colorTextShelves, textFont)
        draw.rectangle([(245, 815), (1485, 925)], outline=colorShelves, width=3)
        draw.line([(865, 815), (865, 925)], fill=colorShelves, width=3)
        draw.text((500, 860), u"Shelf 3m", colorTextShelves, textFont)
        draw.text((1100, 860), u"Shelf 1.5m", colorTextShelves, textFont)
        draw.rectangle([(245, 1090), (1485, 1200)], outline=colorShelves, width=3)
        draw.line([(865, 1090), (865, 1200)], fill=colorShelves, width=3)
        draw.text((500, 1135), u"Shelf 3m", colorTextShelves, textFont)
        draw.text((1100, 1135), u"Shelf 1.5m", colorTextShelves, textFont)

        #Front Counter
        draw.rectangle([(floorWidth - boundaryWidth - counterWidth, boundaryHeight), (floorWidth - boundaryWidth, boundaryHeight + counterHeight)], width=3, outline=colorCounter)
        counterTextWidth, counterTextHeight = textFont.getsize("Counter")
        counterTextImage = Image.new("RGBA", (counterTextWidth, counterTextHeight), (0, 0, 0, 0))
        ImageDraw.Draw(counterTextImage).text((0, 0), "Counter", colorTextCounter, textFont)
        counterTextImage = counterTextImage.rotate(90, expand=1)
        draw.bitmap((floorWidth - boundaryWidth - (counterWidth / 2) - (counterTextImage.width / 2), boundaryHeight + (counterHeight / 2) - (counterTextImage.height / 2)), counterTextImage, fill=(0, 0, 0, 255))

        return image